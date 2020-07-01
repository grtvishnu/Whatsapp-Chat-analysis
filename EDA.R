install.packages("rwhatsapp")
library(rwhatsapp)
library(ggplot2); theme_set(theme_minimal()) #actually you can set any ggplot2 themes in here
library(lubridate)
library(ggimage)
library(tidytext)
library(stopwords)
library(tidyverse)
# Load Data -----------------------------------------------------------------------------------

#import and check structure of data
chat <- rwa_read("chat.txt") %>% 
        filter(!is.na(author)) 

# Number of messages

chat %>%
        mutate(day = date(time)) %>%
        count(author) %>%
        ggplot(aes(x = reorder(author, n), y = n, fill=author)) +
        geom_bar(stat = "identity") +
        ylab("") + xlab("") +
        coord_flip() +
        ggtitle("Number of messages")

# Messages per day

chat %>%
        mutate(day = date(time)) %>%
        count(day) %>%
        ggplot(aes(x = day, y = n)) +
        geom_bar(stat = "identity") +
        ylab("") + xlab("") +
        ggtitle("Messages per day")


# Most often used emotes

emoji_data <- rwhatsapp::emojis %>% # data built into package
        mutate(hex_runes1 = gsub("\\s[[:alnum:]]+", "", hex_runes)) %>% # ignore combined emojis
        mutate(emoji_url = paste0("https://abs.twimg.com/emoji/v2/72x72/", 
                                  tolower(hex_runes1), ".png"))

chat %>%
        unnest(emoji) %>%
        count(author, emoji, sort = TRUE) %>%
        group_by(author) %>%
        top_n(n = 6, n) %>%
        left_join(emoji_data, by = "emoji") %>% 
        ggplot(aes(x = reorder(n,emoji), y = n, fill = author)) +
        geom_col(show.legend = FALSE) +
        ylab("") +
        xlab("") +
        coord_flip() +
        geom_image(aes(y = n + 20, image = emoji_url)) +
        facet_wrap(~author, ncol = 2, scales = "free_y") +
        ggtitle("Most often used emojis") +
        theme(axis.text.y = element_blank(),
              axis.ticks.y = element_blank())

# Most often used words

to_remove <- c(stopwords(language = "en"),
               "media",
               "omitted",
               "ref",
               "dass",
               "schon",
               "mal",
               "android.s.wt",'ahhh','hmm','kk','k','aa','Aa','Ehh', 'aahhh', 'enn', 'nee','aa�', 'aaa','njn','ee',
               'avide','eyy','avide','apo','appo','ipo','okey','oru','nale','ath','ind','oke','onnum','aahh','pole',
               'nthaa','illaa','athe','ivide','poyi','ini','nalla','alla','alle','https','oo','the', 'enik','inne',
               'ithe','inn','ippo','good','onnum','and')        


# Most often used words

chat %>%
        unnest_tokens(input = text,
                      output = word) %>%
        filter(!word %in% to_remove) %>%
        count(author, word, sort = TRUE) %>%
        group_by(author) %>%
        top_n(n = 6, n) %>%
        ggplot(aes(x = reorder_within(word, n, author), y = n, fill = author)) +
        geom_col(show.legend = FALSE) +
        ylab("") +
        xlab("") +
        coord_flip() +
        facet_wrap(~author, ncol = 2, scales = "free_y") +
        scale_x_reordered() +
        ggtitle("Most often used words")        

# Important words used

chat %>%
        unnest_tokens(input = text,
                      output = word) %>%
        select(word, author) %>%
        filter(!word %in% to_remove) %>%
        mutate(word = gsub(".com", "", word)) %>%
        mutate(word = gsub("^gag", "9gag", word)) %>%
        count(author, word, sort = TRUE) %>%
        bind_tf_idf(term = word, document = author, n = n) %>%
        filter(n > 10) %>%
        group_by(author) %>%
        top_n(n = 6, tf_idf) %>%
        ggplot(aes(x = reorder_within(word, n, author), y = n, fill = author)) +
        geom_col(show.legend = FALSE) +
        ylab("") +
        xlab("") +
        coord_flip() +
        facet_wrap(~author, ncol = 2, scales = "free_y") +
        scale_x_reordered() +
        ggtitle("Important words used")

# Lexical Diversity

chat %>%
        unnest_tokens(input = text,
                      output = word) %>%
        filter(!word %in% to_remove) %>%
        group_by(author) %>%
        summarise(lex_diversity = n_distinct(word)) %>%
        arrange(desc(lex_diversity)) %>%
        ggplot(aes(x = reorder(author, lex_diversity),
                   y = lex_diversity,
                   fill = author)) +
        geom_col(show.legend = FALSE) +
        scale_y_continuous(expand = (mult = c(0, 0, 0, 500))) +
        geom_text(aes(label = scales::comma(lex_diversity)), hjust = -0.1) +
        ylab("unique words") +
        xlab("") +
        ggtitle("Lexical Diversity") +
        coord_flip()        
       

# output csv for using Word_cloud.py 

chat_py <- chat %>% 
        select(author,text)
write_csv(chat_py,"chat_py.csv") 
