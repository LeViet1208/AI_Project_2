class InputHolder:
    def __init__(self, input_name):
        f = open(input_name, "r")
        lines = f.readlines()
        f.close()

        self.world_size = int(lines[0])
        self.world_array = []

        for i in range(1, len(lines)):
            linelist = lines[i].split('.')
            for i in range(len(linelist)):
                linelist[i] = linelist[i].replace(' ', '')
            self.world_array.append(linelist)