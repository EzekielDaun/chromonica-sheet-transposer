import argparse
import os
import re


class base12_note(object):  # convert single note to base-12 number
    def __init__(
        self,
        string=None,
        value=None,
        scale=0,
    ):
        self.__note2num = {
            "1": 0,
            "#1": 1,
            "2": 2,
            "#2": 3,
            "3": 4,
            "#3": 5,
            "4": 5,
            "#4": 6,
            "5": 7,
            "#5": 8,
            "6": 9,
            "#6": 10,
            "7": 11,
            "#7": 12,
        }
        self.__num2note = {
            0: "1",
            1: "#1",
            2: "2",
            3: "#2",
            4: "3",
            5: "4",
            6: "#4",
            7: "5",
            8: "#5",
            9: "6",
            10: "#6",
            11: "7",
        }
        if value is not None:
            self.__value = value
            self.scale = int(value / 12) if value >= 0 else int(value / 12) - 1
            self.__string = None
        else:
            self.scale = scale
            self.__string = string
            parser = re.compile(r"#?\d")
            self.__value = self.__note2num[parser.findall(string)[
                0]] + scale * 12

    def __str__(self):
        value = self.__value % 12
        brackets = ("[", "]") if self.scale >= 0 else ("(", ")")
        result = str(self.__num2note[value])
        for i in range(abs(self.scale)):
            result = brackets[0] + result + brackets[1]
        return result

    def __call__(self):
        print(
            "string=",
            self.__string,
            "scale=",
            self.scale,
            "value=",
            self.__value,
        )

    def __add__(self, v):
        return base12_note(
            value=self.__value + v,
        )


def parse_line(string):
    l = []
    scale = 0
    temp = None
    for char in string:
        if char == "#":
            temp = char
        elif char == "(" or char == "]":
            scale -= 1
        elif char == ")" or char == "[":
            scale += 1
        elif char in ("1", "2", "3", "4", "5", "6", "7"):
            note = (
                base12_note(string=str(temp) + char, scale=scale)
                if temp
                else base12_note(string=char, scale=scale)
            )
            l.append(note)
            temp = None
        else:
            l.append(char)
    return l


parser = argparse.ArgumentParser(description="A chromonica sheet transposer.")

parser.add_argument(
    "files",
    nargs="*",
    default=[
        "input.txt",
    ],
    help="file(s) to be converted. Default = \"input.txt\"",
)
parser.add_argument("-o", "--offset", type=int, required=True, help="number of semi-tones to transpose")
parser.add_argument(
    "-p", "--path", type=str, default=r"Converted", help="output path"
)
# parser.add_argument("-t", "--test")

args = parser.parse_args()

orgPath = os.getcwd()

if __name__ == "__main__":

    offset = args.offset

    for fileName in args.files:
        # open input file
        try:
            inputFile = open(fileName, "r")
        except FileNotFoundError:
            print(f"Error: {fileName} does not exist.")
            os._exit(1)

        # create output directory
        try:
            path = args.path
            os.chdir(path)
        except FileNotFoundError:
            print(f"Creating output directory: {os.getcwd()}\{path}")
            os.makedirs(path)
            os.chdir(path)

        # create output file
        (name, ext) = os.path.splitext(inputFile.name)
        name += f"_{offset:+}{ext}"
        outputFile = open(name, "w")

        string = "  "
        while string != "":
            string = inputFile.readline()
            result = ""
            for i in parse_line(string):
                if isinstance(i, base12_note):
                    i += offset
                result += str(i)
            outputFile.write(result)

        print(f"Processed {inputFile.name} with offset {offset:+}!")
        inputFile.close()
        outputFile.close()

        # return to initial working directory
        os.chdir(orgPath)
