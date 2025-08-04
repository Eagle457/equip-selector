import streamlit as st

st.set_page_config(page_title="裝備推薦工具", layout="centered")
st.title("⚔️ 裝備推薦工具")
st.markdown("根據敵人血量、攻速與普攻傷害，自動推薦 **龍骨劍** 或 **雷電戟**")

hp = st.number_input("🔢 敵人血量", min_value=100, max_value=50000, value=10000, step=100)
atk_speed = st.slider("⚡ 普攻間隔（秒）", min_value=0.05, max_value=1.0, value=0.3, step=0.05)
base_damage = st.number_input("🎯 每次普攻基礎傷害", min_value=100, max_value=10000, value=1000, step=50)

bone_extra_cooldown = 0.3
bone_extra_rate = 0.08
thunder_fixed_extra = 87
thunder_third_extra = 430
thunder_third_cooldown = 0.3

def simulate_bone(hp, atk_speed, base_dmg):
    time = 0
    attacks = 0
    total_damage = 0
    last_extra_time = -bone_extra_cooldown
    hp_left = hp

    while hp_left > 0:
        time += atk_speed
        attacks += 1
        dmg = base_dmg
        if time - last_extra_time >= bone_extra_cooldown:
            dmg += hp_left * bone_extra_rate
            last_extra_time = time
        hp_left -= dmg
        total_damage += dmg

    return round(time, 3), attacks, round(total_damage)

def simulate_thunder(hp, atk_speed, base_dmg):
    time = 0
    attacks = 0
    total_damage = 0
    last_third_time = -thunder_third_cooldown
    hp_left = hp

    while hp_left > 0:
        time += atk_speed
        attacks += 1
        dmg = base_dmg + thunder_fixed_extra
        if attacks % 3 == 0 and time - last_third_time >= thunder_third_cooldown:
            dmg += thunder_third_extra
            last_third_time = time
        hp_left -= dmg
        total_damage += dmg

    return round(time, 3), attacks, round(total_damage)

bone_time, bone_attacks, bone_total = simulate_bone(hp, atk_speed, base_damage)
thunder_time, thunder_attacks, thunder_total = simulate_thunder(hp, atk_speed, base_damage)

st.markdown("---")
st.subheader("🧪 龍骨劍")
st.markdown(f"- 擊殺時間：`{bone_time} 秒`")
st.markdown(f"- 攻擊次數：`{bone_attacks} 次`")
st.markdown(f"- 總傷害值：`{bone_total}`")

st.subheader("🧪 雷電戟")
st.markdown(f"- 擊殺時間：`{thunder_time} 秒`")
st.markdown(f"- 攻擊次數：`{thunder_attacks} 次`")
st.markdown(f"- 總傷害值：`{thunder_total}`")

st.markdown("---")
if bone_time < thunder_time:
    st.success("✅ **推薦使用：龍骨劍 🐉**")
elif thunder_time < bone_time:
    st.success("✅ **推薦使用：雷電戟 ⚡**")
else:
    st.info("⚖️ 兩者表現相同，可自由選擇")

st.markdown("---")
st.caption("由 ChatGPT 根據模擬邏輯製作")
