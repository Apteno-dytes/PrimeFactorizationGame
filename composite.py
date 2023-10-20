import PySimpleGUI as sg
import random
import time

# 定数
USED_PRIME = [2, 3, 5]  # 使う素数
MAX_PRIME_TIMES = 3  # 使う素数の最大乗数
START_TIME = 30  # 制限時間

# ターゲットとなる数を作成する


def create_new_number():
    ret_num = 1
    for n in USED_PRIME:
        ret_num *= n ** random.randint(0, MAX_PRIME_TIMES)
    if ret_num == 1:
        ret_num = USED_PRIME[0]
    return ret_num

# タイトル画面


def title():
    layout = [
        [sg.Column([[sg.Text('合成数破壊ゲーム', font=('メイリオ', 24))]], justification='c')],
        [sg.Column([[sg.Button('Start', font=('メイリオ', 18))]],
                   justification='c', vertical_alignment='center')],
        [sg.Column([[sg.Button('Exit', font=('メイリオ', 12))]],
                   justification='r', vertical_alignment='center')]
    ]
    window = sg.Window('合成数破壊ゲーム', layout, size=(400, 200), font=('メイリオ', 18))

    while True:
        event, values = window.read()
        if event == 'Start':
            game()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

# ゲーム画面


def game():
    # 初期化
    left_time = START_TIME
    score = 0
    layout = [
        [sg.Column([[sg.Text('残り時間：'), sg.Text('0', key='-TIME-'), sg.Text('秒')]],
                   justification='c')],
        [sg.Column(
            [[sg.Text('30', font=('Arial', 96), key='-TARGET-')]], justification='c')],
        [sg.Column([[sg.Button(str(USED_PRIME[0]), size=(3, 1), font=('Arial', 54)), sg.Button(
            str(USED_PRIME[1]), size=(3, 1), font=('Arial', 54)), sg.Button(str(USED_PRIME[2]), size=(3, 1), font=('Arial', 54))]], justification='c')],
        [sg.Column([[sg.Text('スコア：'), sg.Text('0', key='-SCORE-')]],
                   justification='c')],
        [sg.Column([[sg.Button('Exit')]], justification='r')]
    ]
    window = sg.Window('バッテリー状態', layout, size=(600, 500),
                       font=('メイリオ', 18), no_titlebar=True)
    window.read(timeout=0)
    window['-TIME-'].update(str(START_TIME))
    window['-SCORE-'].update(str(score))

    # ゲーム開始カウントダウン
    for i in range(3, 0, -1):
        window['-TARGET-'].update(str(i))
        window.read(timeout=0)
        time.sleep(1)

    # ゲーム本編
    target_num = create_new_number()
    current_num = target_num
    window['-TARGET-'].update(str(current_num))
    real_start_time = time.time()
    while left_time > 0:
        if current_num == 1:
            target_num = create_new_number()
            current_num = target_num
            window['-TARGET-'].update(str(current_num))
        left_time = START_TIME - (time.time() - real_start_time)
        window['-TIME-'].update('{:.2f}'.format(round(left_time, 2)))
        event, values = window.read(timeout=0)
        for n in USED_PRIME:
            if event == str(n):
                if current_num % n == 0:
                    current_num //= n
                    score += 1
                    window['-TARGET-'].update(str(current_num))
                    window['-SCORE-'].update(str(score))
                else:  # ミスしたとき
                    score -= 0.5
                    window['-SCORE-'].update(str(score))

        if event == 'Exit' or event == sg.WIN_CLOSED:
            window.close()
            return
    # タイムアップ後処理
    window['-TARGET-'].update("Time's up!")
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            window.close()
            return

# メイン関数


def main():
    title()


if __name__ == '__main__':
    main()
