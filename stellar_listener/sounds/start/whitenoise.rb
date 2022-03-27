# Start Whitenoise v0.1
define :whitenoise_sound do
    play rrand(50, 95), attack: 0.25, release: 0.75, amp: 1
    sleep 0.25
end

in_thread(name: :whitenoise) do
    use_synth :noise
    loop do
        whitenoise_sound
    end
end
