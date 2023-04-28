import numpy
from aws_lambda_powertools import Logger
from numpy import round
from scipy.signal import iirdesign, sosfiltfilt
from tdt import StructType

from src.main.models.block import Block
from src.main.constants import CONFIG

logger = Logger(child=True)


def process_block(data: StructType):
    logger.info("Processing Block")
    trial_size: float = CONFIG.get("trial_size", 0.0)

    block_data: Block = Block(data)

    sampling_rate: numpy.float64 = block_data.streams.lfpx.fs
    lfp_data_stream: numpy.ndarray = block_data.streams.lfpx.data
    channels: list[int] = block_data.streams.lfpx.channels
    trial_start_times: numpy.ndarray = block_data.epocs.get("SPAT").onset

    inverse_sampling = 1 / sampling_rate

    spatial_frequency = block_data.epocs.get("SPAT").data[0]
    contrast = block_data.epocs.get("CONT").data[0]
    orientation = block_data.epocs.get("ORNT").data[0]

    filter_boi = iirdesign(
        ftype="butter",
        fs=sampling_rate,
        output="sos",
        wp=55,
        ws=65,
        gpass=0.1,
        gstop=0.1,
    )

    temp_filter_data: numpy.ndarray = numpy.dot(a=lfp_data_stream, b=0)

    for index in range(0, len(temp_filter_data)):
        temp_filter_data[index] = sosfiltfilt(sos=filter_boi, x=lfp_data_stream[index])

    lfp_data_stream: numpy.ndarray = temp_filter_data

    exp_duration = inverse_sampling * len(lfp_data_stream[1])

    x_axis = numpy.arange(start=0.0, step=inverse_sampling, stop=exp_duration)
    trial_x_axis = numpy.arange(start=0.0, step=inverse_sampling, stop=trial_size)

    number_of_trials = len(trial_start_times)
    truncate_start = 0
    trial_ticks: int = int(round(trial_size * round(sampling_rate)))

    logger.info(
        msg="trial_ticks",
        trial_ticks=trial_ticks,
        trial_ticks_type=trial_ticks.__class__,
    )

    average_channel_data: numpy.ndarray = numpy.zeros([16, trial_ticks])

    logger.info(
        msg="Data",
        lfp=lfp_data_stream,
        spatial_frequency=spatial_frequency,
        contrast=contrast,
        orientation=orientation,
        x_axis=x_axis,
        trial_x_axis=trial_x_axis,
        trial_ticks=trial_ticks,
        trial_size=trial_size,
        number_of_trials=number_of_trials,
        truncate_start=truncate_start,
        average_channel_data=average_channel_data,
    )

    temp_snippet_start = numpy.argmax(a=(x_axis >= trial_start_times[0]))
    temp_snippet_end = temp_snippet_start + trial_ticks

    for channel in channels:
        offset_channel: int = channel - 1

        temp_channel_data: numpy.ndarray = numpy.zeros(
            [number_of_trials, trial_ticks + 1]
        )

        for trial in range(truncate_start, number_of_trials + truncate_start - 1):
            if (trial_start_times[trial] + trial_size) < exp_duration:
                temp_channel_data[trial] = lfp_data_stream[offset_channel][
                    temp_snippet_start : temp_snippet_end + 1
                ]

                if trial == truncate_start:
                    experiment_start = numpy.argmax(
                        a=(x_axis >= trial_start_times[trial])
                    )

                    logger.info(
                        msg="Experiment Start Set.", experiment_start=experiment_start
                    )

                if trial == number_of_trials + truncate_start - 1:
                    experiment_end = (
                        numpy.argmax(a=(x_axis >= trial_start_times[trial]))
                        + trial_ticks
                    )

                    logger.info(
                        msg="Experiment End Set.", experiment_end=experiment_end
                    )

        temp_channel_data = temp_channel_data[truncate_start:]
        average_channel_data[offset_channel] = numpy.mean(temp_channel_data)

    logger.info(msg="Channel Data", average_channel_data=average_channel_data)
