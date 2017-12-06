data = "your
data
here"


def check_words_uniqie(line)
    words = line.split(" ")
    return words == words.uniq
end

total_count = 0

for line in data.split("\n")
    if check_words_uniqie(line)
        total_count += 1
    end
end 

puts total_count
