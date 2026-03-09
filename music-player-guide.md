# 🎵 Mopidy 音乐播放器 - Docker 配置文件

## 使用方法

1. 在 NAS 上打开文件管理器
2. 进入 `/vol1/1000/Docker/music-player/` 文件夹
3. 创建新文件 `docker-compose.yml`
4. 复制以下内容并粘贴

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  # Mopidy 音乐服务器
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
    ports:
      - 6681:80
    restart: unless-stopped
    networks:
      - music-network

networks:
  music-network:
    driver: bridge
```

---

## 部署步骤

1. **保存文件** 后，打开 Docker 应用
2. 进入 **Compose** 标签页
3. 点击 **新增项目**
4. 填写：
   - 项目名称：`music-player`
   - 路径：`/vol1/1000/Docker/music-player`
   - 勾选 ✅ **创建项目后立即启动**
5. 点击 **确认**

---

## 访问地址

部署成功后：
- **Web 播放器**: http://flu.jesson.online:6681
- **Mopidy API**: http://flu.jesson.online:6680

---

## 功能特点

✅ 支持 Spotify、SoundCloud、YouTube  
✅ 支持本地音乐文件  
✅ 漂亮的 Iris Web 界面  
✅ 手机/平板适配  
✅ 无需登录即可使用  

---

**创建时间**: 2026-03-08  
**维护者**: 璐sir
