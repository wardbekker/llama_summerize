# Gong call transcript summarisation example

This example shows how LLAMA can be used to summarize gong call transcripts

## Usage

- Download LLAMA model from https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q5_K_S.bin and place it in a ./models folder
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- On Mac M1, M2 etc make sure to build llama-cpp-python like this: `CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --force llama-cpp-python`. This will build the Metal version of LLAMA which is much faster than the CPU version.
- Run the summarization script: `python summarize.py <gong_transcript_html_file> <key_speaker_name> <output_file>`

## Example

Go to any Gong call, click on the transcript tab, and save the HTML file. Then run the following command:

```
python summarize.py gong-transcript.html "Ward" summary.txt
```

(Main) Speaker name is used for semi-intelligent chunking of the text. 

After a coffee or two this will result in a new text file 'summary.txt' with the summary of the call. At the bottom of the file you will have a total summary of the call, and above that you will have a summary of each chunk of the call.