<div align="center">
<img src="logo.jpg" width=400>
</div>

<p align="center">
🌐 <a href="https://seed.bytedance.com/seed1_8"> Homepage</a>&nbsp&nbsp | &nbsp&nbsp📄 <a href="./Seed-1.8-Modelcard.pdf">Paper</a>
</p>

Today, we are excited to introduce **Seed1.8** , developed to support generalized real-world agency. The model is designed to retain core LLM
and VLM capabilities while extending them toward multi-turn interaction and task execution. Rather than introducing task-specific agent pipelines, Seed1.8 emphasizes integration of perception, reasoning, and action within a single model.

## Highlights

- **Strong Base Capabilities.** Seed1.8 maintains competitive performance on standard LLM and VLM benchmarks, including reasoning, complex instruction following, knowledge coverage, and multimodal understanding. These capabilities provide the foundation for downstream agentic behavior.
- **Unified Agentic Interaction and Multi-Step Execution.** Seed1.8 supports search, code generation and execution within a unified agentic interface. The model is designed to perform iterative decision making over multiple steps, where intermediate results from retrieval, code execution, and environment interaction inform subsequent actions. Search capabilities enable information gathering and evidence synthesis from external sources, while code-centric execution supports structured computation, program modification, and tool orchestration. Native visual perception further allows the model to interpret and interact with visual interfaces—such as screenshots, documents, charts, and videos—enabling direct operation in software environments when programmatic APIs are unavailable.
- **Latency- and Cost-Aware Inference.** Interactive deployment introduces constraints on response time and computational overhead, particularly for multimodal and long-context inputs. Seed1.8 provides configurable thinking modes to balance inference depth and latency, and incorporates optimized visual encoding to reduce token consumption for image and video inputs.
- **Evaluation Aligned with Practical Use.** Model development and validation are guided by a combination of public benchmarks and internal evaluations derived from high-value application domains. These evaluations span foundational capabilities, multimodal understanding, and agentic workflows, enabling assessment across a range of realistic usage patterns.

## Notice

**Call for Bad Cases:** If you have encountered any cases where the model performs poorly, we would greatly appreciate it if you could share them in [the issue](https://github.com/ByteDance-Seed/Seed-1.8/issues).

## Seed1.8 Cookbook

The Seed1.8 cookbook is designed to help you start using the Seed1.8 API with diverse code samples. Our flagship Seed1.8 has been deployed on [Volcano Engine](https://www.volcengine.com/product/doubao). After obtaining your `API_KEY`, you can use the examples in this cookbook to rapidly understand and leverage the diverse capabilities of our Seed1.8.

### Quick Start

- [x] Cookbook for [Code Agents](./Code)
- [x] Cookbook for [Search Agents](./Search)
- [x] Cookbook for [Multimodal Search Agents](./MM-Search)
- [x] Cookbook for [MCP Tool Use Agents](./MCP)
- [x] Cookbook for [Thinking with Images Agents](./Thinking_with_Images)
- [x] Cookbook for [2D Grounding](./Grounding)
- [x] Cookbook for [3D Understanding](./3D-Understanding)
- [x] Cookbook for [Video Understanding](./Video)

## License

This repo is under [Apache-2.0 License](./LICENSE).

## About [ByteDance Seed Team](https://seed.bytedance.com/)

Founded in 2023, ByteDance Seed Team is dedicated to crafting the industry's most advanced AI foundation models. The team aspires to become a world-class research team and make significant contributions to the advancement of science and society.
