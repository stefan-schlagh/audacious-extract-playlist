import sys,os
import traceback
from urllib.parse import unquote, urlparse
import argparse
from shutil import copy

def main():
    ExtractPlaylist()

class ExtractPlaylist:
    def __init__(self):
        try:
            self.executeOptions()
        except Exception as e:
            traceback.print_exc()
            self.Log("Exited with an error: " + str(e))
    
    def Log(self,val):
        print(val)

    def executeOptions(self):
        # parse args
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="the mode that should be used, modes:  extractSongTitles | extractSongs",type=str)
        parser.add_argument("--src", help="location of the playlist file",type=str)
        parser.add_argument("--dest", help="destination of the files",type=str)
        args = parser.parse_args()

        mode = args.mode
        self.srcPath = args.src
        self.dest = args.dest

        if(mode == "extractSongTitles"):
            self.extractPlaylistSongTitles()
            self.writeSongTitles()
        elif(mode == "extractSongs"):
            self.extractPlaylistSongs()
            self.copySongs()
        else:
            self.Log("No valid mode specified!")
    def extractPlaylistSongTitles(self):
        f = open(self.srcPath)
        content = f.read().split("\n")
        f.close()
        titles = []
        i=0
        for line in content:
            if('uri=' in line and not 'uri=' in content[i + 1]):
                line = line.replace("uri=", "")
                utf8 = unquote(line)
                a = urlparse(utf8)
                title = os.path.splitext(os.path.basename(a.path))[0]
                if not title in titles and not "Kopie" in title:
                    titles.append(title)
                    #titles.append(os.path.splitext(os.path.basename(a.path))[0])
            i = i + 1
        self.songTitles = titles
    
    def writeSongTitles(self):
        f = open(self.dest,"wb")
        for title in self.songTitles:
            f.write((title + '\r\n').encode("utf-8"))
        f.close()

    def extractPlaylistSongs(self):
        f = open(self.srcPath)
        content = f.read().split("\n")
        f.close()
        #extract title
        self.title = unquote(content[0].replace("title=", ""))
        # extract songs
        songs = []
        titles = []
        i=0
        for line in content:
            if('uri=' in line and not 'uri=' in content[i + 1]):
                url = unquote(line.replace("uri=", ""))
                title = os.path.splitext(os.path.basename(urlparse(url).path))[0]
                if not title in titles and not "Kopie" in title:
                    titles.append(title)
                    songs.append({
                        "url": url,
                        "title": title
                    })
            i = i + 1
        self.songs = songs
        self.songTitles = titles

    def copySongs(self):
        # create folder
        path = self.dest + "/" + self.title
        if not os.path.exists(path):
            os.makedirs(path)
        # copy songs
        for song in self.songs:
            try:
                copy(song['url'].replace("file://",""),path)
            except Exception as e:
                traceback.print_exc()
                self.Log("error: " + str(e) + " ... moving on")

if __name__ == "__main__":
   main()
