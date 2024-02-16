from tiktoken import encoding_for_model

class Chunk:
    def __init__(self, model="gpt-4-1106-preview"):
        self.model = model
        if model == "gpt-4-1106-preview":
            self.max_token = 128000
        self.encoder = encoding_for_model(self.model)
    
    def chunk(self, content: str, else_text=""):
        content_encoding = self.encoder.decode(self.encoder.encode(content))
        else_text_encoding = self.encoder.encode(else_text)
        max_token = self.max_token - len(else_text_encoding)
        
        chunks = []
        while len(content_encoding) > 0:
            chunks.append(content_encoding[0:max_token])
            content_encoding = content_encoding[max_token:]

        return chunks