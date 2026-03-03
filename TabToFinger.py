import xml.etree.ElementTree as ET
import argparse
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="reads music XML file (from musescore) and outputs a list of tuples")
    parser.add_argument('file',type=str)
    args=parser.parse_args()
    notelist=[]
    try:
        file=open(args.file,encoding="utf8")
    except FileNotFoundError:
        print("Error: file does not exist")
    else:
        with file:
            tree=ET.parse(args.file)
            root=tree.getroot()
            part=root[-1]
            print(part[0][2])
            print( f"the bpm is {part[0].find('direction').find('sound').get('tempo')}")
            for measure in part:
                for note in measure.findall('note'):
                    for spec in note.iter("technical"):
                        string=int(spec[0].text)
                        fret=int(spec[1].text)
                        notelist.append((string, fret))
            print(notelist)