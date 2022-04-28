from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig


def setup_receiver():
    # Lora Parameters
    RFM95_RST = 27
    RFM95_SPIBUS = SPIConfig.rp2_1
    RFM95_CS = 5
    RFM95_INT = 28
    RF95_FREQ = 902.5  # 868 OU 902.5-927.5 MHz
    RF95_POW = 20
    CLIENT_ADDRESS = 0
    SERVER_ADDRESS = 0

    # initialise radio
    lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ,
                tx_power=RF95_POW, acks=True)

    # set callback
    lora.on_recv = _on_receive_callback

    # set to listen continuously
    lora.set_mode_rx()


def _on_receive_callback(payload):
    # This is our callback function that runs when a message is received
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))


if __name__ == "__main__":
    setup_receiver()
    while True:
        # loop and wait for data
        sleep(0.5)
        print("Dormindo")


