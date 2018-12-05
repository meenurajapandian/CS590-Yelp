#### Cleaning businesses data ------------------------------------------------------------------------------------------------------

# All businesses except those that are definitely not restaurants

business <- read.csv("yelp_academic_dataset_business.csv")
business <- as.data.frame(business)
df <- business[business$state =="NV",]
df <- as.data.frame(df[df$attributes.HairSpecializesIn=="",])
df <- df[df$attributes.AcceptsInsurance != "True",]
df <- df[df$attributes.ByAppointmentOnly != "True",]
df <- df[df$is_open==1,]
df <- df[df$attributes.AcceptsInsurance=="",]
df <- df[df$attributes.ByAppointmentOnly=="",]
df$state <- NULL
df$attributes.AcceptsInsurance <- NULL
df$attributes.ByAppointmentOnly <- NULL
df<- df[-which(df$attributes.RestaurantsReservations=="" & df$attributes.RestaurantsDelivery=="" & df$attributes.OutdoorSeating=="" & df$attributes.DriveThru=="" & df$attributes.RestaurantsReservations=="" & df$attributes.RestaurantsTakeOut==""),]
df$attributes.HairSpecializesIn <- NULL
df$is_open <- NULL
df$categories <- gsub("[[:punct:]]+","",df$categories)
df <- df[-which(grepl("Automotive", df$categories)),]
df <- df[-which(grepl("Floral", df$categories)),]
df <- df[-which(grepl("Event", df$categories)),]
df <- df[-which(grepl("Arts", df$categories)),]
df <- df[-which(grepl("Grocery", df$categories)),]

df <- droplevels(df)

write.csv(df, "./nevada_files/nevada_business.csv", fileEncoding = "UTF-8")
bid <- unique(df$business_id)

rm(business)
rm(df)


#### Reading reviews data --------------------------------------------------------------------------------------------------------
library(dplyr)

# Reading only reviews for businesses from the previous list

con = file("yelp_academic_dataset_review.csv","r")
i <- 1
n_rev <- data.frame()
review <- read.csv(con, nrows=1e4,stringsAsFactors = F, header = T)
df <- review[review$business_id %in% bid ,]
n_rev <- bind_rows(n_rev, df)
rnames <- colnames(n_rev)
while(i){
  review <- read.csv(con, nrows=1e4,stringsAsFactors = F, header = F, col.names = rnames)
  df <- review[review$business_id %in% bid ,]
  n_rev <- bind_rows(n_rev, df)
  if(nrow(review) != 1e4){break}
}
close(con)

write.csv(n_rev, "./nevada_files/nevada_review.csv", fileEncoding = "UTF-8")
uid <- unique(n_rev$user_id)

#### Reading User data ---------------------------------------------------------------------------------

# Only those users that have give reviews for the select businesses

con = file("yelp_academic_dataset_user.csv", "r")
i <- 1
n_user <- data.frame()
user <- read.csv(con, nrows=1e4, stringsAsFactors = F, header = T)
df <- user[user$user_id %in% uid ,]
n_user <- bind_rows(n_user, df)
unames <- colnames(n_user)
while(i){
  user <- read.csv(con, nrows=1e4, stringsAsFactors = F, header = F, col.names = unames)
  df <- user[user$user_id %in% uid ,]
  n_user <- bind_rows(n_user, df)
  if(nrow(user) != 1e4){break}
}
close(con)

n_user <- n_user[n_user$review_count>10,]
n_user <- droplevels(n_user)
write.csv(n_user, "./nevada_files/nevada_user.csv", fileEncoding = "UTF-8")

#### Reading User data 2---------------------------------------------------------------------------------

# Reading all users who have some friends

con = file("yelp_academic_dataset_user.csv", "r")
i <- 1
n_user <- data.frame()
user <- read.csv(con, nrows=1e4, stringsAsFactors = F, header = T)
df <- user[-which(user$friends=="None"),]
n_user <- bind_rows(n_user, df)
unames <- colnames(n_user)
while(i){
  user <- read.csv(con, nrows=1e4, stringsAsFactors = F, header = F, col.names = unames)
  df <- user[-which(user$friends=="None"),]
  n_user <- bind_rows(n_user, df)
  if(nrow(user) != 1e4){break}
}
close(con)

n_user <- n_user[n_user$review_count>10,]
n_user <- droplevels(n_user)
write.csv(n_user, "./nevada_files/nevada_user_2.csv", fileEncoding = "UTF-8")

#### Further cleaning -----------------------------------------------------------------------------------

dfb <- read.csv("./nevada_files/nevada_business.csv", stringsAsFactors = F, fileEncoding = "UTF-8")
dfb <- as.data.frame(dfb)
dfb <- dfb[which(grepl("Food", dfb$categories)),]
dfb <- droplevels(dfb)
bid <- unique(dfb$business_id)

dfb1 <- read.csv("nevada_business_cleaned.csv", stringsAsFactors = F, fileEncoding = "UTF-8")
bid <- unique(dfb1$business_id)

dfb2 <- read.csv("nevada_business_cleaned_v2.csv", stringsAsFactors = F, fileEncoding = "UTF-8")
bid <- unique(dfb2$business_id)

dfr <- read.csv("./nevada_files/nevada_review.csv", stringsAsFactors = F, fileEncoding = "UTF-8")
dfr <- dfr[dfr$business_id %in% bid ,]
uid <- unique(dfr$user_id)


dfu <- read.csv("./nevada_files/nevada_user.csv", fileEncoding = "UTF-8", stringsAsFactors = F)
dfu <- dfu[dfu$user_id %in% uid,]

# dfu2 <- data.frame()
# for (i in 1:length(uid)){
#   dfu2 <- bind_rows(dfu2, dfu[grepl(uid[i], dfu$friends, fixed=TRUE),])
# }

dfu <- dfu[dfu$review_count < 6000 ,]
dfu <- dfu[dfu$review_count > 105 ,]

dfu <- droplevels(dfu)
uid <- unique(dfu$user_id)
dfr <- dfr[dfr$user_id %in% uid ,]
#dfu1 <- dfu1[dfu1$friends!="None",]

#dfu <- union(dfu1, dfu2)

#write.csv(dfu, "users_filtered.csv", fileEncoding = "UTF-8")

#### Making network ----------------------------------------------------------------------------------------------------------------------
df <- dfr
user <- df %>% group_by(user_id) %>% summarise(n=n()) %>% as.data.frame()
uid <- user$user_id[user$n > 10]
df <- df[df$user_id %in% uid ,]

review <- vector("list")
for (i in 1:length(uid)){
    review[[uid[i]]] <- df$business_id[df$user_id==uid[i]] 
}
k <- 1
edgelist <- data.frame(matrix(ncol=3,nrow=0))
colnames(edgelist) <- c("user1","user2","strength")
for (i in 1:length(uid)){
  print(i)
  for (j in i:length(uid)){
    t <- length(intersect(review[[uid[i]]],review[[uid[j]]]))
    if (t>0){
      edgelist[k,] <- c(uid[i],uid[j],t)
      k <- k + 1
    }
  }
}
write.csv(edgelist,"usernetwork.csv", fileEncoding = "UTF-8")

dfu <- dfu[dfu$user_id %in% uid,]
dfu$comp_tile <- dfu$compliment_cool + dfu$compliment_cute + dfu$compliment_funny + dfu$compliment_hot + dfu$compliment_list +
  dfu$compliment_more + dfu$compliment_note + dfu$compliment_photos + dfu$compliment_plain + dfu$compliment_profile + dfu$compliment_writer

dfu$friend <- lengths(regmatches(dfu$friends, gregexpr(",", dfu$friends)))

for (i in 1:length(uid)){
  dfu$businesses[dfu$user_id == uid[i]] <- paste(review[[df$user_id[i]]], collapse=", ")
}

dfu <- dfu %>% mutate(comp_rank = percent_rank(comp_tile))
dfu.d <- dfu[, c("user_id", "name", "yelping_since", "review_count", "friend", "comp_rank", "businesses")]
write.csv(dfu.d, "userdetails.csv", fileEncoding = "UTF-8")

