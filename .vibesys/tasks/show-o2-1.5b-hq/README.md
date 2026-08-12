Repository-native VibeSys task for Show-o2 1.5B HQ.

Run from the vllm-omni repository root:

```bash
vibesys --project . --task show-o2-1.5b-hq \
  --runs-dir /work/vibesys-runs --local
```

This bundle targets `showlab/show-o2-1.5B-HQ`, a Show-o2 text-to-image
checkpoint. The reference folder uses a pinned git submodule for the official
Show-o inference source and keeps model weights out of git. On first real use,
the loader downloads:

- `showlab/show-o2-1.5B-HQ` into the repo HF cache and links it as
  `reference/model`
- `Wan-AI/Wan2.1-T2V-14B/Wan2.1_VAE.pth` through `huggingface_hub`
- the Qwen2.5 tokenizer/config and SigLIP weights used by the official model

For a local HTTP smoke test that does not download weights:

```bash
# Terminal 1
uv run python /path/to/vibesys/examples/model-serving/show_o2_mock_server.py --port 8000

# Terminal 2
uv run python .vibesys/tasks/show-o2-1.5b-hq/benchmark/benchmark.py \
  --url http://localhost:8000 --warmup-requests 1 --num-requests 1 --steps 1
```

The mock server is part of the VibeSys development repository, not this fork.
For a real run, install the task dependencies from
`.vibesys/tasks/show-o2-1.5b-hq/requirements.txt` and start a server backed by
the reference model instead of the mock server.
