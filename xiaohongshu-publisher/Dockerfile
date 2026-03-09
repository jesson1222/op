FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

WORKDIR /app

# 配置国内 pip 镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制脚本
COPY publish.py .
COPY cookie_manager.py .

# 创建数据目录
RUN mkdir -p /app/data /app/images

WORKDIR /app

# 首次运行显示浏览器，后续可改 headless
CMD ["python", "publish.py"]
