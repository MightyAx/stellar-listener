define :polaris_sound do
    sample :bass_thick_c, attack: 0.25, release: 0.75, amp: 0
end
  
in_thread(name: :polaris_signal) do
    loop do
        polaris_sound
        sleep 1
    end
end
