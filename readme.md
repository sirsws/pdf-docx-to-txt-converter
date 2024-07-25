# PDF and DOCX to TXT Converter
# PDF和DOCX转TXT工具

A Python script to convert PDF and DOCX files to TXT format in batch. It's particularly useful for preparing training data for large language models.

这是一个Python脚本，用于将PDF和DOCX文件批量转换为TXT格式。它特别适用于准备大型语言模型的训练数据集。

## Features
## 功能特点

- Support for PDF (text and image) and DOCX file conversion
- OCR technology for processing image PDFs
- Multi-threaded processing for improved efficiency
- Automatic detection and fixing of small files (potentially failed conversions)
- Text preprocessing, including removal of extra whitespace and punctuation unification

- 支持PDF（文本和图片）和DOCX文件转换
- 使用OCR技术处理图片PDF
- 多线程处理提高效率
- 自动检测并修复小文件（可能是处理失败的文件）
- 文本预处理，包括去除多余空白、统一标点符号等

## Installation Requirements
## 安装要求

Before running this script, make sure to install the following dependencies:

在运行此脚本之前，请确保安装了以下依赖：

pip install -r requirements.txt

Note: paddleocr may require additional setup. Please refer to the [PaddleOCR official documentation](https://github.com/PaddlePaddle/PaddleOCR).

注意：paddleocr可能需要额外的设置，请参考[PaddleOCR的官方文档](https://github.com/PaddlePaddle/PaddleOCR)。

## Usage
## 使用方法

1. Clone this repository:
   克隆此仓库：

git clone https://github.com/your-username/pdf-docx-to-txt-converter.git
cd pdf-docx-to-txt-converter

2. Run the script:
运行脚本：

python converter.py <input_folder> <output_folder> [--max_workers MAX_WORKERS] [--size_threshold SIZE_THRESHOLD]

Parameters:
参数说明：
- `input_folder`: Input folder path containing PDF and DOCX files to be converted
- `output_folder`: Output folder path for saving converted TXT files
- `--max_workers`: (Optional) Maximum number of worker threads, default is 4
- `--size_threshold`: (Optional) Small file threshold (KB), default is 10KB

- `input_folder`：输入文件夹路径，包含待转换的PDF和DOCX文件
- `output_folder`：输出文件夹路径，用于保存转换后的TXT文件
- `--max_workers`：（可选）最大工作线程数，默认为4
- `--size_threshold`：（可选）小文件阈值（KB），默认为10KB

Example:
示例：

python converter.py ./input_docs ./output_texts --max_workers 6 --size_threshold 20

## Notes
## 注意事项

- Processing large quantities or large files may take a considerable amount of time
- OCR processing may require significant computational resources
- It's recommended to use a dedicated machine or run during off-hours when processing large amounts of files

- 处理大量或大型文件可能需要较长时间
- OCR处理可能需要较高的计算资源
- 建议在处理大量文件时使用专用机器或在非工作时间运行

## Contributing
## 贡献

We welcome issue reports, feature requests, and code contributions. Please follow these steps:

欢迎提交问题报告、功能请求和代码贡献。请遵循以下步骤：

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## License
## 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。