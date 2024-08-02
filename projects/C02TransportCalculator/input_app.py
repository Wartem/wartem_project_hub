from flask import render_template, request, redirect, url_for

def handle_input():
    if request.method == 'POST':
        distance = request.form['distance']
        return redirect(url_for('CO2TransportCalculator.show_result', distance=distance))
    return render_template('input.html')