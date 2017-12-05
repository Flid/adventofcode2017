from mojov3.register import RegisterCommunicator

reg = RegisterCommunicator()

TARGET_X = 361527

CMD_NEW_VALUE = 0
CMD_READ_RESULT = 1

reg.register_write(address=CMD_NEW_VALUE, data=[TARGET_X])

print(reg.register_read(address=CMD_READ_RESULT, size=1))
