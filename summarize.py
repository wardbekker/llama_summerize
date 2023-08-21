import os
import html2markdown
import re
from llama_cpp import Llama

CONTEXT = 4096 # 4k context length
TOKEN_CHARACTER_RATIO = 2
MAX_CHUNK_LENGTH = int(CONTEXT * TOKEN_CHARACTER_RATIO) - 200
MODEL_NAME = "./models/llama-2-13b-chat.ggmlv3.q5_K_S.bin"
LLAMA_PROMPT_TEMPLATE = """SYSTEM: You create summaries of business meeting transcript. Do not repeat the actual conversations. Only respond in bulleted lines, in the line format. Summarize in the third person only, that is very important: "* (Speaker Name) key points."
USER: INSERT_PROMPT_HERE
ASSISTANT:"""

# init the llama model
llm = Llama(model_path=MODEL_NAME, n_ctx=CONTEXT, n_batch=224, n_gpu_layers=1, verbose=True)

def main():
    # if no command line arguments are given, print usage and exit
    if len(os.sys.argv) < 3:
        print(f"Usage: {os.sys.argv[0]} transcript_file")
        print(f"Usage: {os.sys.argv[0]} speaker_name")
        print(f"Usage: {os.sys.argv[0]} summary_file")
        exit()

    # first command line value is the transcript file
    transcript_file = os.sys.argv[1]
    # second command line value is the speaker name
    speaker_name = os.sys.argv[2]
    # third command line value is the summary file
    summary_file = os.sys.argv[3]
    
    summarisations = summerize_chunks(parse_gong_transcript(transcript_file, speaker_name), summary_file)

    # TODO: support more chunks in the final summerisation step
    overall_summary = summarize(chunk_text("".join(summarisations), speaker_name)[0])

    # write overall summary to the summary file
    with open(summary_file, "a") as f:
        f.write("\n\nOverall summary:\n\n")
        f.write(overall_summary)
    print("done")


# function that will summarize a piece of text 
def summarize(text):    
    prompt = 'Summarize the key points of the following business meeting transcript as a flat list of lines. This is very important.: ' + text
    prompt = LLAMA_PROMPT_TEMPLATE.replace('INSERT_PROMPT_HERE', prompt)
    output = llm(prompt, max_tokens=-1, echo=False, temperature=0.7, top_p=0.1, top_k=40, repeat_penalty=1.176)
    llm.reset()
    text = output['choices'][0]['text']
    # remove text until the semicolon, to remove stuff like: Sure! Here is a summary of the conversation in a single sentence:
    return text[text.find(":") + 1:]

def chunk_text(text, speaker_name):
    # remove whitespace longer than 2 characters
    text = re.sub(r'\s{2,}', ' ', text)

    # remove all newlines
    text = text.replace("\n", " ")

    # split the text into chunks. Make sure not to split in the middle of a sentence
    max_length = MAX_CHUNK_LENGTH
    chunks = []
    while len(text) > max_length:
        split_index = text[max_length:].find(f" {speaker_name} ") + max_length
        chunks.append(text[:split_index])
        text = text[split_index + 1:]

    chunks.append(text)
    
    # print the amount of chunks generated
    print(f"generated {len(chunks)} chunks")
    return chunks

def parse_gong_transcript(transcript_file, speaker_name):
    html = ""

    with open(transcript_file, "r") as f:
        html = f.read()

    # extract all the divs with the class "monologue"
    # monologues = re.findall(r'<div class="monologue">(.+?)</div>', html, re.DOTALL)
    monologues = re.findall(r'<div class="monologue">(.+?)</div>', html, re.DOTALL)

    # remove any remaining html tags with a regex
    text = re.sub('<[^<]+?>', '', " ".join(monologues))

    return chunk_text(text, speaker_name)

def summerize_chunks(chunks, target_file):
    # let's summarize the conversation per chunk
    summarisations = []

    print("starting summarisation.....")    
    for i, chunk in enumerate(chunks):
        print("\033[92m" + f"summarising chunk {i} of {len(chunks)}" + "\033[0m")
        # print out sample of the chunk
        print("\033[93mChunk sample: " + chunk[:100] + "..." + "\033[0m")

        new_sum = summarize(chunk)
        print("\033[93m" + new_sum + "\033[0m")
        summarisations.append(new_sum)

    # write summarisations to a text file
    with open(target_file, "w") as f:
        # add header with name of transcript file
        f.write(f"\n\nSummarisations of {target_file}\n\n")
        
        for i, sum in enumerate(summarisations):
            f.write(sum)
    return summarisations

if __name__ == "__main__":
    main()