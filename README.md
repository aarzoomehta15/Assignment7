# Mashup Generator - Assignment 7

## Objective
This project implements a **command-line Python program** that generates a **mashup audio file** by downloading songs of a given singer from YouTube, trimming each audio clip to a fixed duration, and merging them into a single output file.

The program demonstrates **input validation**, **exception handling**, and **audio processing** using third-party Python libraries.

---

## Methodology

1. **Command-Line Input**
   The program accepts the following arguments:
   ```
   python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
   ```
      
2. **Input Validation**
- Number of videos must be greater than 10  
- Audio duration must be greater than 20 seconds  
- Invalid inputs terminate execution with a message

3. **Audio Download**
- Uses the `yt-dlp` PyPI library to search and download YouTube videos related to the given singer
- Videos are converted directly to MP3 format
- Download errors caused by restricted or unavailable videos are handled gracefully

4. **Audio Processing**
- Uses the `pydub` library to trim the first `Y` seconds of each audio file
- Trimmed audio clips are merged sequentially to form a mashup

5. **Exception Handling**
- If some videos fail to download due to YouTube restrictions, the program continues processing available files
- The program avoids crashing and reports the status appropriately
