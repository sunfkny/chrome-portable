from typing import Iterable

import streamlit as st


def select_versions(label_major: str, label_version: str, versions: Iterable[str]):
    major_versions = sorted(set(int(version.split(".")[0]) for version in versions))
    selected_major_version = st.selectbox(
        label_major,
        options=major_versions,
    )
    if selected_major_version:
        selected_version = st.selectbox(
            label_version,
            options=sorted(version for version in versions if version.startswith(f"{selected_major_version}.")),
        )
        return selected_version
