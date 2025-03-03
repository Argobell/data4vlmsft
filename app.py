# webui/app.py
import streamlit as st
import os
import json
from src.dataset_builder import DatasetBuilder
from typing import List, Optional

# Streamlit Web UI
def main():
    # 设置页面标题和图标
    st.set_page_config(
        page_title="ShareGPT 数据集生成器",
        page_icon="📊",
        layout="wide"
    )

    # 页面标题
    st.title("📊 ShareGPT 数据集生成器")
    st.markdown("使用 Hugging Face 数据集生成 ShareGPT 格式的多模态数据集。")

    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        dataset_path = st.text_input("数据集路径", value=r"D:\data4vlm\data\hwe-text")
        save_dir = st.text_input("图像保存目录", value="./downloaded_images")
        num_samples = st.number_input("样本数量", min_value=1, value=10)
        st.markdown("---")
        st.markdown("### 自定义 Instructions")
        num_instructions = st.number_input("输入 Instructions 的数量", min_value=0, value=0)
        custom_instructions = []
        for i in range(num_instructions):
            instruction = st.text_area(
                f"Instruction {i + 1}",
                value="",
                key=f"instruction_{i}"
            )
            custom_instructions.append(instruction)
        st.session_state.custom_instructions = custom_instructions

    # 初始化 session_state
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'dataset' not in st.session_state:
        st.session_state.dataset = None

    # 数据集预览
    st.header("🔍 数据集预览")
    if st.button("加载数据集"):
        if not dataset_path:
            st.error("请填写数据集路径！")
        else:
            try:
                with st.spinner("正在加载数据集..."):
                    builder = DatasetBuilder(dataset_path, save_dir)
                    st.session_state.dataset = builder.dataset
                    st.success(f"数据集加载成功！数据集大小：{len(st.session_state.dataset)}")
            except Exception as e:
                st.error(f"加载数据集时出错：{e}")

    # 如果数据集已加载，显示当前样本
    if st.session_state.dataset is not None:
        st.subheader("📄 当前样本")
        col1, col2 = st.columns([1, 2])
        with col1:
            # 显示当前索引的样本图像
            item = st.session_state.dataset[st.session_state.current_index]
            image = item['image']
            st.image(image, caption=f"样本 {st.session_state.current_index + 1} 图像", use_container_width=True)
        with col2:
            # 显示当前索引的样本文本
            text = item['text']
            st.write(f"**文本：** {text}")

        # 翻页按钮
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 上一张"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
        with col2:
            if st.button("➡️ 下一张"):
                if st.session_state.current_index < len(st.session_state.dataset) - 1:
                    st.session_state.current_index += 1

    # 生成数据集
    st.header("🛠️ 生成数据集")
    if st.button("生成数据集"):
        if not dataset_path or not save_dir:
            st.error("请填写数据集路径和保存目录！")
        else:
            try:
                with st.spinner("正在生成数据集..."):
                    builder = DatasetBuilder(dataset_path, save_dir)
                    sharegpt_data = builder.build_dataset(num_samples, st.session_state.custom_instructions)

                    # 保存数据集
                    os.makedirs(save_dir, exist_ok=True)
                    output_path = os.path.join(save_dir, "sharegpt_dataset.json")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(sharegpt_data, f, ensure_ascii=False, indent=4)
                    st.success(f"数据集生成成功！保存路径：{output_path}")

                    # 提供下载按钮
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="📥 下载数据集",
                            data=f,
                            file_name="sharegpt_dataset.json",
                            mime="application/json"
                        )
            except Exception as e:
                st.error(f"生成数据集时出错：{e}")

if __name__ == "__main__":
    main()