import math
from utilities.exceptions import MathExpressionError
import logging

c_light_velocity = 299792458.0


def convert_to_decibel(val):
    try:
        dB = 10 * math.log10(val)
    except ValueError as e:
        logging.error('Ошибка конвертации в децибелы значения: ' + str(val))
        raise MathExpressionError(e.args)
    return dB


def convert_from_decibel(val):
    return math.pow(10, val / 10)


def gain(pin, pout, osnr_out):
    # исправлено 06.08.2018
    # в старой реализации не хватало единицы, добавляемой к OSNR в знаменателе:
    # return pout - pin + convert_to_decibel( 1-convert_from_decibel(-osnr_out) )
    return pout - pin + convert_to_decibel(1 - 1 / (convert_from_decibel(osnr_out) + 1))


def noise_figure(pin, pout, osnr_out, osnr_in):
    try:
        osnr_sum = - convert_to_decibel(1 / convert_from_decibel(osnr_out) - 1 / convert_from_decibel(osnr_in))
        # исправлено 30.10.2017 со слов Шихалиева И. В данную функцию уже передаётся реальное значение OSNR,
        # учитывающее Pase
        # в старой реализации Гайновым В. была допущена ошибка с вычитанием единиц в знаменателях:
        # osnr_sum = convert_to_decibel(1/(convert_from_decibel(osnr_out)-1) - 1/(convert_from_decibel(osnr_in)-1))
    # последующее деление на 0 будет событием странным
    except ZeroDivisionError as e:
        logging.error('Ошибка при вычислении суммарного osnr -- в знаменателе ноль:\n'
                      '\tOSNR_in = {} dB; OSNR_out = {} dB'.format(osnr_in, osnr_out))
        raise MathExpressionError(e.args)

    nf = convert_from_decibel(58 + pin - osnr_sum)
    g = convert_from_decibel(- gain(pin, pout, osnr_out))
    nf_real = convert_to_decibel(nf + g)
    return nf_real


def osnr_from_signal_and_noise(psignal_pnoise_level_diff, resolution):
    return convert_to_decibel(
        convert_from_decibel(psignal_pnoise_level_diff) - 1) + convert_to_decibel(resolution / 0.1)


def convert_wavelength_to_thz(nm):
    nm = float(nm)
    return c_light_velocity / nm / 1000


def convert_freq_to_wavelength(thz):
    thz = float(thz)
    return c_light_velocity / thz / 1000


def convert_wavelength_to_ch(nm, plan_50_ghz=False):
    nm = float(nm)
    freq_thz = convert_wavelength_to_thz(nm)
    channel = freq_thz * 10.0 - 1900.0
    if plan_50_ghz:
        channel = int(2 * channel + 0.5) / 2
    else:
        channel = int(channel + 0.5)
    return channel


def convert_channel_to_wavelength(channel):
    """Конвертирует номер канала в длину волны.

    :param channel: Номер канала.
    :type channel: int | float | str

    Если канал приходит строкой, то она должна содержать один из символов '.' или 'e'. Например, "21.5", "21e".
    Если "21e", то получаем канал 21+0.5=21.5
    """
    valid_char = ['.', 'e']
    channel_as_str = ''
    if isinstance(channel, str):
        symbol_in_channel = [i for i in valid_char if i in channel] if not isinstance(
            channel, (int, float,)
        ) else []
        if symbol_in_channel:
            try:
                channel_as_str = channel
                if 'e' in symbol_in_channel:
                    channel = int(channel.split(symbol_in_channel[0])[0]) + 0.5
                    logging.debug(
                        "Номер канала преобразован из вида {} в {} для конвертирования его в частоту.".format(
                            channel_as_str, channel
                        ))
                if '.' in symbol_in_channel:
                    channel = float(channel)
                    logging.debug(
                        "Номер канала преобразован из вида {} в {} для конвертирования его в частоту.".format(
                            channel_as_str, channel
                        ))
            except:
                logging.warning("Не могу сконвертировать номер канала {} в частоту.".format(channel))
                return
    freq_thz = channel / 10 + 190
    return convert_freq_to_wavelength(freq_thz)


def inverf(p):
    a = 8 * (math.pi - 3) / (4 - math.pi) / 3 / math.pi
    z = math.log(1 - math.pow(p, 2))
    b = a * z + 4 / math.pi
    ret = math.sqrt((math.sqrt(math.pow(b, 2) - 4 * a * z) - b) / a)
    return ret
