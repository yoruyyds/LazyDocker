@echo off
echo ========================================
echo LazyDocker Control - 打包脚本
echo ========================================
echo.

echo [1/3] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo 清理完成！
echo.

echo [2/3] 开始打包（这可能需要几分钟）...
pyinstaller LazyDocker.spec
echo.

if exist dist\LazyDocker.exe (
    echo [3/3] 打包成功！
    echo.
    echo ========================================
    echo 输出文件: dist\LazyDocker.exe
    for %%A in (dist\LazyDocker.exe) do echo 文件大小: %%~zA 字节
    echo ========================================
    echo.
    echo 提示：双击 dist\LazyDocker.exe 运行程序
    echo.
) else (
    echo [3/3] 打包失败！请检查错误信息。
    echo.
)

pause
