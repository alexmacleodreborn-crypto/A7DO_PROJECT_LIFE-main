import time
import streamlit as st


def st_autorefresh(interval: int = 0, limit: int | None = None, key: str = "autorefresh") -> int:
    if interval <= 0:
        return 0

    count_key = f"{key}_count"
    last_key = f"{key}_last"

    if count_key not in st.session_state:
        st.session_state[count_key] = 0
    if last_key not in st.session_state:
        st.session_state[last_key] = time.time()

    elapsed = time.time() - st.session_state[last_key]
    if elapsed >= interval / 1000:
        if limit is None or st.session_state[count_key] < limit:
            st.session_state[count_key] += 1
            st.session_state[last_key] = time.time()
            st.experimental_rerun()

    return st.session_state[count_key]
