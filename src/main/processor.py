import numpy
from aws_lambda_powertools import Logger
from numpy import round
from scipy.signal import iirdesign, sosfiltfilt
from tdt import StructType

from src.main.models.block import Block

logger = Logger(child=True)


def process_block(data: StructType):
    logger.info("Processing Block")
    trial_size = 1.2

    block_data: Block = Block(data)

    sampling_rate: numpy.float64 = block_data.streams.lfpx.fs
    lfp_data_stream: numpy.ndarray = block_data.streams.lfpx.data
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

    logger.info(temp_filter_data)

    lfp_data_stream: numpy.ndarray = temp_filter_data

    exp_duration = inverse_sampling * len(lfp_data_stream[1])

    x_axis = numpy.arange(start=0.0, step=inverse_sampling, stop=exp_duration)
    trial_x_axis = numpy.arange(start=0.0, step=inverse_sampling, stop=trial_size)

    number_of_trials = len(trial_start_times)
    truncate_start = True
    trial_ticks = round(trial_size * round(sampling_rate))
    average_channel_data = numpy.zeros(16, trial_ticks)

    logger.info(f"Data: {lfp_data_stream}")
