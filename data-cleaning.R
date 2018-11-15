#### Cleaning businesses data ------------------------------------------------------------------------------------------------------
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
