# Project Overview & Quick Demonstration

Welcome to **md2pdf**. This sample document illustrates how various Markdown syntax elements render into the final PDF output.

---

## 1. Callout Alert Boxes

> [!NOTE]
> This is an informational callout block. It uses subtle slate blue borders and backgrounds.

> [!TIP]
> Use fast swipe gestures with tight durations (e.g. 100ms) for high-performance UI automation.

> [!WARNING]
> Ensure device authorization is confirmed before initiating mass package uninstallation.

---

## 2. Structured Data & Tables

| Category | Parameter | Default Value | Notes |
| :--- | :--- | :---: | :--- |
| **System** | Screen Resolution | `1080 x 2412` | Full HD+ Display |
| **Network** | Wi-Fi State | `Enabled` | Dual-band 2.4 / 5 GHz |
| **Audio** | Volume Level | `Level 12` | Media channel |

---

## 3. Syntax Highlighted Code Blocks

```powershell
# Fast PIN Unlock with zero artificial animation delay:
adb shell "input keyevent KEYCODE_WAKEUP && input swipe 540 1800 540 540 50 && input text 000000 && input keyevent 66"

# Universal Hotspot Toggle:
adb shell "input keyevent KEYCODE_WAKEUP && cmd statusbar expand-settings && sleep 0.5 && input tap 786 528"
```

---

## 4. Checklist & Task Management

- [x] Implement zero-dependency Markdown parser
- [x] Connect headless Edge/Chromium engine
- [x] Configure A4 print media styling
- [ ] Add PDF watermark support

---

## 5. Inline Formatting

You can write ***bold italic text***, ~~strikethrough text~~, `inline code snippets`, and [hyperlinks](https://github.com).
