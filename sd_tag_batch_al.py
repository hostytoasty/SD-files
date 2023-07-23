import gradio as gr
from modules import scripts, shared, deepbooru
from modules.processing import process_images


class Script(scripts.Script):
    def title(self):
        return "Img2img batch interrogator - Edited"

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        override_prompt = gr.Textbox(label="Override Prompt", lines=1, elem_id=self.elem_id("override"))
        in_front = gr.Checkbox(label="Prompt in front", elem_id=self.elem_id("in_front"))
        # prompt_weight = gr.Slider(
        #     0.0, 1.0, value=1, step=0.1, label="interrogator weight"
        # )
        use_deepbooru = gr.Checkbox(label="Use deepbooru", elem_id=self.elem_id("deepbooru"))
        #return [in_front, prompt_weight, use_deepbooru,override_prompt]
        return [in_front, use_deepbooru, override_prompt]

    #def run(self, p, in_front, prompt_weight, use_deepbooru,override_prompt):
    def run(self, p, in_front, use_deepbooru, override_prompt):
        prompt = ""
        if use_deepbooru:
            prompt = deepbooru.model.tag(p.init_images[0])
        else:
            prompt = shared.interrogator.interrogate(p.init_images[0])
        print(p.prompt)

        #prompt='test'
        p.prompt=override_prompt

        if p.prompt == "":
            p.prompt = prompt
        elif in_front:
            p.prompt = f"{p.prompt}, {prompt}"
        else:
            p.prompt = f"{prompt}, {p.prompt}"

        print(f"Prompt: {p.prompt}")
        return process_images(p)
