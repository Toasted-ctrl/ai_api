from wakeonlan import send_magic_packet

def boot_server(mac_address: str) -> None:
    send_magic_packet(mac_address)