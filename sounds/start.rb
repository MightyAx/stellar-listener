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

# Start Vega v0.1
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