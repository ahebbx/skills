# Codex 安装服务商品主图案例

这是已经成功生成的提示词，适合复现本次黑灰绿风格。其他业务需要按实际服务改写文案，不继承未经用户确认的服务承诺。

```text
Use case: ads-marketing
Create a polished Chinese ecommerce product hero image for an independent Codex installation and configuration service. Square composition. Premium charcoal black background, crisp white typography with fresh green accents, generous negative space, excellent readability at thumbnail size.
Upper section: very large word "Codex", followed by prominent Chinese headline "安装配置服务".
Center: an elegant three-dimensional laptop in a subtle three-quarter view, showing a simplified dark code terminal and a completed installation progress indicator with a green check. Soft studio lighting and restrained green glow.
Lower section: three clean service labels, exactly "软件安装", "环境配置", "上手指导".
Bottom tagline exactly "让 AI 编程更快上手".
Professional editorial typography and balanced layout, precise Chinese text. No prices, QR codes, official endorsement badges, fabricated official logo, watermarks, subscription claims, or free/unlimited promises. This is a commercial service listing image, not an instructional diagram.
```

本次经验：密钥不在环境变量中，但存在于 Codex 的 `auth.json`；供应商地址在选中的 `model_providers` 配置中。使用 SDK 的 `OPENAI_BASE_URL` 和子进程专用 `OPENAI_API_KEY` 即可调用兼容的图片接口。此经验不能推导出所有聊天供应商都支持生图；要以实际请求结果为准。
