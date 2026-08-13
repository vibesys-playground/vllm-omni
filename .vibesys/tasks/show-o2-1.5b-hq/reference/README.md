Reference bundle for Show-o2 1.5B HQ.

Required files:
- `.vibesys/tasks/show-o2-1.5b-hq/reference/reference.py`: local loader and
  generation wrapper
- `.vibesys/tasks/show-o2-1.5b-hq/reference/config.json`: Show-o2 model config
  copied from the HF checkpoint
- `.vibesys/tasks/show-o2-1.5b-hq/reference/meta.json`: pinned model and Wan VAE
  metadata
- `.vibesys/tasks/show-o2-1.5b-hq/reference/Show-o/`: git submodule for the
  official Show-o repository, pinned to
  commit `45a5a2de01d1ebd10cd5864d29310a76476cdf23`; the wrapper imports from
  its `show-o2/` subdirectory

Initialize it, including any nested submodules, and validate the checkout from
the vllm-omni repository root:

```bash
git submodule update --init --recursive \
  .vibesys/tasks/show-o2-1.5b-hq/reference/Show-o
python .vibesys/tasks/show-o2-1.5b-hq/preflight.py
```

The wrapper exposes `ShowO2Model.from_pretrained(...)`, `generate_text(...)`,
and `generate_image(...)`. It lazily downloads weights if
`.vibesys/tasks/show-o2-1.5b-hq/reference/model` does not exist.
