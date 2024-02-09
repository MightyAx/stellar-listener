define :whitenoise_sound do
    play rrand(50, 95), attack: 0.25, release: 0.75, amp: {amp:.2f}
    sleep 0.25
end
