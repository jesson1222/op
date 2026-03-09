# 🎵 Mopidy 音乐播放器 - HTTPS 配置指南

## 📦 更新后的 docker-compose.yml

我已准备好包含 Nginx Proxy Manager 的配置文件，支持 HTTPS 访问！

---

## 🚀 部署步骤

### 1️⃣ 在 NAS 上创建文件

1. 打开 **文件管理**
2. 进入 `/vol1/1000/Docker/music-player/` 文件夹
3. 创建/更新 `docker-compose.yml` 文件
4. 复制以下完整内容：

```yaml
version: '3.8'

services:
  # 🎵 Mopidy 音乐服务器
  mopidy:
    image: lscr.io/linuxserver/mopidy:latest
    container_name: mopidy
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - ./mopidy/config:/config
      - ./music:/music
    ports:
      - 6600:6600
      - 6680:6680
    restart: unless-stopped
    networks:
      - music-network

  # Iris Web 界面
  mopidy-iris:
    image: xridge/mopidy-iris:latest
    container_name: mopidy-iris
    depends_on:
      - mopidy
    expose:
      - '80'
    restart: unless-stopped
    networks:
      - music-network

  # 🔒 Nginx Proxy Manager
  nginx-proxy-manager:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: nginx-proxy-manager
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./npm/data:/data
      - ./npm/letsencrypt:/etc/letsencrypt
    environment:
      - TZ=Asia/Shanghai
      - DISABLE_IPV6=true
    restart: unless-stopped
    networks:
      - music-network

networks:
  music-network:
    driver: bridge
```

### 2️⃣ 在 Docker 中部署

1. 打开 **Docker** → **Compose**
2. 找到 `music-player` 项目
3. 点击 **停止**（如果正在运行）
4. 点击 **更多** → **重建并启动**
5. 或者删除后重新创建项目

---

## 🔒 配置 HTTPS

### 1️⃣ 登录 Nginx Proxy Manager

- **地址**: `https://flu.jesson.online:81`
- **默认账号**: `admin@example.com`
- **默认密码**: `changeme`
- **首次登录会要求修改密码**

### 2️⃣ 添加 Proxy Host

1. 点击 **Hosts** → **Proxy Hosts** → **Add Proxy Host**

2. **Basic Settings**:
   ```
   Domain Names: music.flu.jesson.online
   Scheme: http
   Forward Hostname / IP: mopidy-iris
   Forward Port: 80
   Cache Assets: ✅ 勾选
   ```

3. **SSL Tab**:
   ```
   SSL Certificate: Request a new SSL certificate
   Email: 你的邮箱
   Domain Names: music.flu.jesson.online
   ✅ I agree to the Terms of Service
   ✅ Force SSL
   ✅ HTTP/2 Support
   ```

4. 点击 **Save**

---

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **音乐播放器** | https://music.flu.jesson.online | HTTPS 加密访问 |
| **Nginx 管理面板** | https://flu.jesson.online:81 | 管理反向代理 |
| **Mopidy API** | http://flu.jesson.online:6680 | 本地 API（不推荐外网） |

---

## 📋 DNS 配置

确保你的域名已解析到 NAS：

```
music.flu.jesson.online  →  NAS 公网 IP
flu.jesson.online        →  NAS 公网 IP
```

---

## 🔧 故障排查

### 端口被占用

如果 80/443/81 端口被占用，修改 nginx-proxy-manager 的 ports：

```yaml
ports:
  - '8080:80'   # HTTP 改为 8080
  - '8181:81'   # 管理面板改为 8181
  - '8443:443'  # HTTPS 改为 8443
```

### 证书申请失败

1. 检查域名 DNS 解析是否正确
2. 确保 80 端口可以从外网访问
3. 查看日志：`docker logs nginx-proxy-manager`

### 无法访问 mopidy-iris

在 Nginx Proxy Manager 中，Forward Hostname 填容器名 `mopidy-iris`，不是 `localhost`。

---

## 🎯 后续优化

### 1. 添加本地音乐

在 NAS 上创建音乐文件夹，挂载到容器：

```yaml
volumes:
  - /vol1/1000/音乐:/music  # 你的音乐文件夹
```

### 2. 配置 Spotify

在 Mopidy 配置文件中添加 Spotify 账号：

文件位置：`./mopidy/config/mopidy.conf`

```ini
[spotify]
enabled = true
username = 你的 Spotify 账号
password = 你的 Spotify 密码
```

### 3. 配置 SoundCloud

```ini
[soundcloud]
enabled = true
explore_cache = 100
```

---

## 📝 文件结构

```
/vol1/1000/Docker/music-player/
├── docker-compose.yml          # 主配置文件
├── mopidy/
│   └── config/
│       └── mopidy.conf         # Mopidy 配置
├── music/                       # 本地音乐文件夹
└── npm/
    ├── data/                    # Nginx 数据
    └── letsencrypt/             # SSL 证书
```

---

**更新时间**: 2026-03-08  
**维护者**: 璐sir  
**版本**: v2.0 (HTTPS)
