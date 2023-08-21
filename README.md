# Gong call transcript summarisation example

This example shows how LLAMA can be used to summarize gong call transcripts

## Usage

- Download LLAMA model from https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_K_S.bin and place it in a ./models folder
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- Run the summarization script: `python summarize.py <gong_transcript_html_file> <key_speaker_name> <output_file>`

## Example

```
python summarize.py gong-transcript.html "Ward" summary.txt
```