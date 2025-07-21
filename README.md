# FocusScreen - 随机专注时钟


基于 PyQt5 实现的随机提示音学习法的 Python 桌面端应用程序。

## 简介

FocusScreen 是一款加入了「**随机提示音**」的 Python 专注计时器应用（基于 PyQt5）。



学习并借鉴下面的内容：

- 灵感来源： [为什么我能每天学习 10 小时](https://www.bilibili.com/video/BV1naLozQEBq/?spm_id_from=333.337.search-card.all.click&vd_source=3af1ac70b2d2ca8e0ae72cb13b3c65d6)
- 项目思路：[Focus - 随机专注时钟（MacOS）](https://github.com/JokerQianwei/Focus/tree/main)



## 代码结构



> FocusScreen                                                                                 
> ├─ src                                                                                      
> │  ├─ assets                                                                                
> │  │  ├─ font                                                                               
> │  │  │  └─ DSEG7Classic-Bold.ttf                                                           
> │  │  ├─ rest                                                                               
> │  │  │  ├─ bg01.jpg                                                                        
> │  │  │  ├─ bg02.jpg                                                                        
> │  │  │  └─ bg03.jpg                                                                        
> │  │  ├─ wav                                                                                
> │  │  │  ├─ mixkit-intro-transition-1146.wav                                                
> │  │  │  ├─ mixkit-light-rain-loop-2393.wav                                                 
> │  │  │  ├─ mixkit-little-birds-singing-in-the-trees-17.wav                                 
> │  │  │  └─ mixkit-melodical-flute-music-notification-2310.wav                              
> │  │  └─ icon-app.jpg                                                                       
> │  ├─ core                                                                                  
> │  │  ├─ sound                                                                              
> │  │  │  └─ sound_player.py                                                                 
> │  │  ├─ statistics                                                                         
> │  │  ├─ time                                                                               
> │  │  │  ├─ time_logic.py                                                                   
> │  │  │  └─ time_state.py                                                                   
> │  │  └─ utils                                                                              
> │  │     ├─ const.py                                                                        
> │  │     └─ utils.py                                                                        
> │  ├─ dist                                                                                  
> │  │  └─ Focus.exe                                                                          
> │  ├─ widget                                                                                
> │  │  ├─ rest                                                                               
> │  │  │  └─ rest_overlay.py                                                                 
> │  │  ├─ setting                                                                            
> │  │  │  └─ setting_dialog.py                                                               
> │  │  └─ timer                                                                              
> │  │     └─ timer_ball.py                                                                   
> │  └─ main.py                                                                               
> └─ README.md                                                                                

## 核心功能

---

- Tip：目前使用 Pyinstaller 打包 exe 程序，涵括静态资源，未来将解耦资源和程序。
- 🔔 **微休息提醒**：默认专注总周期设置为 90 分钟，每隔 3-5 分钟响起提示音乐，提醒短暂休息 15 秒，随后自动二次提示，引导回归专注状态（所有参数可调）
  - [ ] TODO：解决 `QTimer` 导致的 60:00 自动回调时间为 00:00 的错误。
  - [ ] TODO：添加 `提醒时间` 会提醒用户 90 分钟的专注时间即将结束，抓紧时间整理目前的工作内容。
- 🖥️ **微休息全屏幕**：全屏幕覆盖功能，在微休息时自动覆盖所有显示器画面，帮助用户强制休息，微休息结束后自动恢复。
  - [ ] TODO：添加 `上传图片` 功能、`自定义文字内容` 功能。
- 🎵 **随机音效**：支持微休息开始的随机提示音效。
  - [ ] TODO：添加 `上传音效` 功能、`自定义选择使用音效` 功能。
- 💻 **系统托盘**：隐藏/显示应用托盘。

- [ ] TODO：📊 **数据统计**。
- [ ] TODO：🎞️ **媒体控制功能**。



## 页面展示

---

![image-20250721185751201](./assets/image-20250721185751201.png)
