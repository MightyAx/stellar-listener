define :polaris_sound do
    sample :bass_thick_c, amp: 0
end
  
in_thread(name: :polaris_signal) do
    loop do
        polaris_sound
        sleep 3
    end
end
