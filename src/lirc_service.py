import logging
import coloredlogs
import subprocess

logger = logging.getLogger("lirc_service")
coloredlogs.install(level='DEBUG', logger=logger)

def runLircCommand(remoteName: str, key: str, repeatCount=1, timeout=2):
    irSendCommand = f'irsend send_once {remoteName} {key} --count {repeatCount}'
    logger.debug(f'Running Command: {irSendCommand}')

    try:
        process = subprocess.run(irSendCommand, timeout=timeout, capture_output=True, shell=True)
        process.check_returncode()
        logger.debug('irsend command executed successfully')
    except subprocess.TimeoutExpired as timeout: 
        logger.warning('The executed irsend command took to long to respond')
        logger.warning('Depending on your configuration, this may be normal')
        logger.warning('especially when using a repeat count > 1.')
        logger.warning(f'IRSend Output: {timeout.output}')
    except subprocess.CalledProcessError as err:
        logger.error('Error while executing the irsend process.')
        logger.error('This may caused due to a missing lirc installation or missconfiguration')
        logger.error(f'IRSend Output: {err.output}')
    except BaseException as ex:
        logger.error('Unknown Error while executing the irsend process.')
        logger.exception(ex)
