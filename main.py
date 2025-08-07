from playwright.sync_api import sync_playwright
import time
import random
import os

# 配置信息（建议使用环境变量存储敏感信息）
SITE_URL = "https://gk2.axkaajanetwork.com/"

USERNAME = os.getenv("email", "YourEmail")  # 从环境变量获取或直接填写
PASSWORD = os.getenv("pwd", "YourPWD")

Checked = False

def sleepTime():
    return random.randint(15, 20)

def auto_sign():
    with sync_playwright() as p:
        # 启动浏览器（headless模式设为False便于调试）

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 访问网站
            page.goto(SITE_URL)

            # 等待登录相关元素加载（根据实际页面调整选择器）
            # 假设需要登录，查找登录表单
            page.wait_for_selector("input[name='email']", timeout=5000)

            # 填写登录表单（根据实际页面调整选择器）
            page.fill("input[name='email']", USERNAME)
            page.fill("input[name='password']", PASSWORD)

            # 提交登录表单（可能需要点击按钮或直接提交）
            print('✅ 填写登录信息成功!')
            time.sleep(sleepTime())
            page.click("button#login_submit")

            # 等待登录后页面加载
            time.sleep(sleepTime())
            try:
                page.wait_for_selector(
                    "h2.text-white.font-weight-bold:has-text('用户中心')",
                    timeout=15000
                )  # 检查登录后一些的元素
                print('✅ 登录成功!')
            except Exception as e:
                print('❌ 登陆失败!')
                print(e)
                return

            # 执行签到操作
            # 查找签到按钮并点击
            try:
                checkin_btn = page.query_selector("#checkin")
                checkin_btn.click()
                print("🔄 正在执行签到...")
            except Exception:
                print('✅ 已经签到过了')
                global Checked
                Checked = True
                return

            # 检查签到结果
            try:    
                page.wait_for_selector(
                    "#swal2-title",
                    timeout=15000
                )  # 检查登录后一些的元素
                print("✅ 签到成功！")
                Checked = True
            except:
                print("⚠️ 签到状态未知，请手动确认")

        except Exception as e:
            print(f"操作失败：{str(e)}")
            # 添加截图功能用于调试
            page.screenshot(path="error.png")

        finally:
            # 关闭浏览器
            browser.close()


if __name__ == "__main__":
    for i in range(5):
        time.sleep(random.randint(50,200)) # 随机登陆时间
        auto_sign()
        if Checked:
            print('✅ 第{}次签到成功'.format(i+1))
            break
        else:
            if i < 4:
                print('❌ 第{}次签到失败, 重试.....'.format(i+1))
            else:
                print('❌ 5次签到失败, 请手动检查!!')
                raise Exception("❌ 5次签到失败, 请手动检查!")
