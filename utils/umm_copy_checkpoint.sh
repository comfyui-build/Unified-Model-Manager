#!/bin/bash
# umm_copy_checkpoint.sh albedobaseXL_v21.safetensors /mnt/chenyu-nvme/umm/checkpoints
# 会将文件拷贝至目录, 并改成  {sha256前2位}/{sha256} 的方式保存

# 检查参数个数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_file> <destination_directory>"
    exit 1
fi

# 源文件和目标目录
SOURCE_FILE="$1"
DEST_DIR="$2"

# 检查目标目录是否存在，如果不存在则创建
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
fi

# 计算源文件的sha256值
SHA256=$(sha256sum "$SOURCE_FILE" | awk '{print $1}')

# 构建目标路径
DEST_PATH="${DEST_DIR}/${SHA256:0:2}/${SHA256}"

# 确保目标路径的目录结构存在
mkdir -p "$(dirname "$DEST_PATH")"

# 拷贝文件到目标路径
cp "$SOURCE_FILE" "$DEST_PATH"

# 在控制台回显sha256
echo "Copied $SOURCE_FILE to $DEST_PATH"
echo "SHA256: $SHA256"

# 如果是 * 作为参数，则处理当前目录下所有文件
if [ "$1" == "*" ]; then
    # 遍历当前目录下的所有文件
    for file in *; do
        if [ -f "$file" ]; then
            # 递归调用脚本自身
            ./$0 "$file" "$DEST_DIR"
        fi
    done
fi