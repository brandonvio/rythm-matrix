class _converter:
    @staticmethod
    def round5str(float_value):
        value = round(float_value, 5)
        return str(value)

    @staticmethod
    def round4str(float_value):
        value = round(float_value, 4)
        return str(value)

    @staticmethod
    def round4(float_value):
        value = round(float_value, 4)
        return value

    @staticmethod
    def round5(float_value):
        value = round(float_value, 5)
        return value
