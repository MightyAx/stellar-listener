define :whitenoise_sound do
  play rrand(50, 95), attack: 0.25, release: 0.75, amp: {white}
  sleep 0.25
end

define :vega_sound do
  sample :drum_bass_hard, amp: {vega}
end
