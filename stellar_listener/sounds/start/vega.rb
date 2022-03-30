define :vega_sound do
    sample :drum_bass_hard, amp: 0
end

in_thread(name: :vega_signal) do
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97].ring
    loop do
        primes.tick.times do
            vega_sound
            sleep 1
        end
        sleep 1
    end
end
