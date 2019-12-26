#### Exploratory Data Analysis ---------------------------------------------------------------------------
library(ggplot2)
library(dplyr)
library(tidyr)
library(ggmap)

df.bus <- read.csv("nevada_business.csv")
colClean <- function(x){ colnames(x) <- gsub("attributes.", "", colnames(x)); x }
df.bus <- colClean(df.bus)

df.bus$DietaryRestrictions <- NULL
df.bus$Open24Hours <- NULL
#assume all ages for empty variables

df.bus$AgesAllowed[which(df.bus$attributes.AgesAllowed=="")] <- "allages"
df.bus$BYOB <- NULL
df.bus$BYOBCorkage <- NULL
df.bus$neighborhood <- NULL
df.bus$BikeParking <- NULL
df.bus$Alcohol <- NULL
df.bus$GoodForDancing <- NULL
df.bus$RestaurantsCounterService <- NULL
df.bus$WiFi <- NULL

df.bus$categories <- gsub("[[:punct:]]+","",df.bus$categories)
df.bus <- df.bus[-which(grepl("Automotive", df.bus$categories)),]
df.bus <- df.bus[-which(grepl("Floral", df.bus$categories)),]
df.bus <- df.bus[-which(grepl("Event", df.bus$categories)),]

df.bus$Ambience <- as.character(df.bus$Ambience)
df.bus$Ambience <- gsub("[[:punct:]]+","", df.bus$Ambience)
df.bus <- df.bus[which(complete.cases(df.bus$latitude)),]
df.bus <- df.bus[which(complete.cases(df.bus$postal_code)),]

colors = c(rep("#CCF2FF",1),rep("#A3E8FF",2),rep("#4DC9FF",2),rep("#0092FF",2),rep("#0000B3",2))
ggplot(df.bus) + geom_histogram(aes(x=stars), fill=colors, color="white", binwidth = 0.5) + 
  xlab("Ratings") + ylab("Frequency") + 
  ggtitle("Histogram of Ratings") + theme_minimal() + 
  theme(panel.grid.major.x = element_blank(), panel.grid.minor.x = element_blank(), 
        plot.title = element_text(size = 18))

lv_map <- ggmap(get_googlemap(center=c(-115.15,36.125), scale=1, zoom=11), extent="normal")
temp <- map[map$longitude > -115.4,]
temp <- temp[temp$longitude < -114.9,]
temp <- temp[temp$latitude > 35.95,]
temp <- temp[temp$latitude < 36.3,]
lv_map + geom_point(aes(x=longitude, y=latitude, color = color), data=temp, size = 0.9) + 
  scale_color_manual(values=c("#0000B3","#0092FF", "#4DC9FF","#A3E8FF", "#CCF2FF")) +
  theme_minimal() +
  theme(legend.position="none",axis.title=element_blank(), axis.text=element_blank(),axis.ticks=element_blank())

lv_map + geom_point(aes(x=longitude, y=latitude), data=temp, size = 0.8, color = "#FE0007") +
  theme_minimal() +
  theme(legend.position="none",axis.title=element_blank(), axis.text=element_blank(),axis.ticks=element_blank())



ggplot(df.bus) + geom_jitter(aes(y=log(review_count), x=as.factor(stars)), fill="yellow")
ggplot(df.bus) + geom_violin(aes(x="",y=review_count))
ggplot(df.bus) + geom_violin(aes(x=attributes.Corkage, y=stars))
ggplot(df.bus) + geom_boxplot(aes(x=attributes.HasTV, y = stars)) 

df.bp <- df.bus
df.bp[,c("city","hours","postal_code","BestNights","attributes","address", "hours.Wednesday","hours.Sunday","hours.Monday","hours.Thursday","hours.Friday","hours.Tuesday","hours.Saturday","categories","name","business_id","Music")]<- NULL
j <- 1
p <- list()
for (i in (1:ncol(df.bp))){
  if(is.factor(df.bp[,i])){
    df.count <- df.bp %>% group_by(df.bp[,i]) %>% summarize(n=n()) %>% mutate(freq = round(100*n/sum(n), digits=2)) %>% as.data.frame()
    p[[j]] <- ggplot(df.bp) + geom_boxplot(aes(x=df.bp[,i], y = stars), width = 0.3, fill="#FF9200", color="#FF9200", alpha = 0.5) + 
            geom_text(data=df.count, aes(x = 1:nlevels(df.count$`df.bp[, i]`), y = 6, label=freq)) + 
            xlab(colnames(df.bp)[i]) + ylab("Rating") +
            theme_minimal() + theme(panel.grid.major.x = element_blank(), panel.grid.minor.x = element_blank())
    ggsave(filename=paste("boxplot",i,".png",sep=""), plot=p[[j]], device=NULL)
    j <- j+1
  }
}


df.bus$RestaurantsAttire[df.bus$RestaurantsAttire=="formal"] <- "dressy"
df.bus$RestaurantsAttire <- droplevels(df.bus$RestaurantsAttire)
ggplot(df.bus) + geom_boxplot(aes(x=RestaurantsAttire, y = stars)) 

df.bus$RestaurantsPriceRange2[df.bus$RestaurantsAttire=="casual" & is.na(df.bus$RestaurantsPriceRange2)] <- 1.5
df.bus$RestaurantsPriceRange2[df.bus$RestaurantsAttire=="" & is.na(df.bus$RestaurantsPriceRange2)] <- 1.6

order1 <- c("","False","True")
order2 <- c("","True","False")


df.corr <- df.bus[,c("business_id", "stars", "review_count", "RestaurantsPriceRange2")]
df.corr$HasTV <- as.numeric(factor(df.bus$HasTV, levels=order1))
df.corr$GoodForGroups <- as.numeric(factor(df.bus$RestaurantsGoodForGroups, levels=order2))
df.corr$GoodForKids <- as.numeric(factor(df.bus$GoodForKids, levels=order2))
df.corr$HappyHour <- as.numeric(factor(df.bus$HappyHour, levels=order2))
df.corr$WheelchairAccessible <- df.bus$WheelchairAccessible
df.corr$WheelchairAccessible[df.corr$WheelchairAccessible==""] <- "False"
df.corr$WheelchairAccessible <- as.numeric(factor(df.bus$WheelchairAccessible, levels=order2))
df.corr$RestaurantsReservations <- as.numeric(factor(df.bus$RestaurantsReservations, levels=order1))
df.corr$Caters <- as.numeric(factor(df.bus$Caters, levels=order1))
df.corr$BusinessAcceptsCreditCards <- as.numeric(factor(df.bus$BusinessAcceptsCreditCards, levels=order2))
df.corr$DogsAllowed <- as.numeric(factor(df.bus$DogsAllowed, levels=order1))
df.corr$DriveThru <- as.numeric(factor(df.bus$DriveThru, levels=order1))
df.corr$OutdoorSeating <- as.numeric(factor(df.bus$OutdoorSeating, levels=order1))
df.corr$RestaurantsDelivery <- as.numeric(factor(df.bus$RestaurantsDelivery, levels=order1))
df.corr$CoatCheck <- as.numeric(factor(df.bus$CoatCheck, levels=order1))
df.corr$RestaurantsTableService <- as.numeric(factor(df.bus$RestaurantsTableService, levels=order1))
df.corr$Noise <- as.numeric(factor(df.bus$NoiseLevel, levels=c("","quiet","average","loud","very_loud")))
df.corr$Smoking <- as.numeric(factor(df.bus$Smoking, levels=c("","yes","no","outdoor")))
df.corr$log_review_count <- log(df.corr$review_count)
df.corr$RestaurantsAttire <- as.numeric(factor(df.bus$RestaurantsAttire, levels=c("","casual","dressy")))

library(corrplot)
png(height=1200, width=1500, pointsize=25, file="corr1.png")
corrplot(cor(df.corr[,2:21]), method="color", order="hclust")
dev.off()

df.bus$BusinessParking <- gsub("[[:punct:]]+","", df.bus$BusinessParking)
df.park <- df.bus[,c("stars","BusinessParking")]
df.park <- df.park %>% separate(BusinessParking, c(NA, "garage", NA, "street", NA, "validated", NA, "lot", NA, "valet"))
df.park <- df.park[which(complete.cases(df.park$garage)),]
df.park$g <- as.numeric(factor(df.park$garage, levels=c("False","True")))
df.park$s <- as.numeric(factor(df.park$street, levels=c("False","True")))
df.park$vi <- as.numeric(factor(df.park$validated, levels=c("False","True")))
df.park$l <- as.numeric(factor(df.park$lot, levels=c("False","True")))
df.park$ve <- as.numeric(factor(df.park$valet, levels=c("False","True")))

M <- cor(df.park[,c("stars","g","s","vi","l","ve")])
colnames(M) <- c("stars","garage","street","validated","lot","valet")
rownames(M) <- c("stars","garage","street","validated","lot","valet")
png(height=1200, width=1500, pointsize=25, file="corr2.png")
corrplot(M, method="color")
dev.off()


df.time <- df.bus[,c("hours.Monday","hours.Tuesday","hours.Wednesday","hours.Thursday","hours.Friday","hours.Saturday","hours.Sunday")]
df.time$stars <- df.bus$stars
df.time <- df.time %>% separate(hours.Monday, c("MonF","MonT"), sep="-")
df.time <- df.time %>% separate(hours.Tuesday, c("TueF","TueT"), sep="-")
df.time <- df.time %>% separate(hours.Wednesday, c("WedF","WedT"), sep="-")
df.time <- df.time %>% separate(hours.Thursday, c("ThursF","ThursT"), sep="-")
df.time <- df.time %>% separate(hours.Friday, c("FriF","FriT"), sep="-")
df.time <- df.time %>% separate(hours.Saturday, c("SatF","SatT"), sep="-")
df.time <- df.time %>% separate(hours.Sunday, c("SunF","SunT"), sep="-")

df.time <- as.data.frame(apply(df.time, 2, function(y) as.numeric(gsub(":","\\.",y))))
df.time$MonT[df.time$MonT==0.00] <- 23.99
df.time$TueT[df.time$TueT==0.00] <- 23.99
df.time$WedT[df.time$WedT==0.00] <- 23.99
df.time$ThursT[df.time$ThursT==0.00] <- 23.99
df.time$FriT[df.time$FriT==0.00] <- 23.99
df.time$SatT[df.time$SatT==0.00] <- 23.99
df.time$SunT[df.time$SunT==0.00] <- 23.99

df.t <- df.time[which(complete.cases(df.time)),]
df.t$MonT[df.t$MonF > df.t$MonT] <- df.t$MonT[df.t$MonF > df.t$MonT]+24
df.t$Mon <- df.t$MonT - df.t$MonF
df.t$TueT[df.t$TueF > df.t$TueT] <- df.t$TueT[df.t$TueF > df.t$TueT]+24
df.t$Tue <- df.t$TueT - df.t$TueF
df.t$WedT[df.t$WedF > df.t$WedT] <- df.t$WedT[df.t$WedF > df.t$WedT]+24
df.t$Wed <- df.t$WedT - df.t$WedF
df.t$ThursT[df.t$ThursF > df.t$ThursT] <- df.t$ThursT[df.t$ThursF > df.t$ThursT]+24
df.t$Thurs <- df.t$ThursT - df.t$ThursF
df.t$FriT[df.t$FriF > df.t$FriT] <- df.t$FriT[df.t$FriF > df.t$FriT]+24
df.t$Fri <- df.t$FriT - df.t$FriF
df.t$SunT[df.t$SunF > df.t$SunT] <- df.t$SunT[df.t$SunF > df.t$SunT]+24
df.t$Sun <- df.t$SunT - df.t$SunF
df.t$SatT[df.t$SatF > df.t$SatT] <- df.t$SatT[df.t$SatF > df.t$SatT]+24
df.t$Sat <- df.t$SatT - df.t$SatF
corrplot.mixed(cor(df.t))
#df.t <- df.t[which(complete.cases(df.t)),]

M <- cor(df.t)
#colnames(M) <- c("stars","garage","street","validated","lot","valet")
#rownames(M) <- c("stars","garage","street","validated","lot","valet")
png(height=1200, width=1500, pointsize=25, file="corr3.png")
corrplot(M, method="color",order="hclust")
dev.off()

ggplot(df.t) + geom_jitter(aes(x=Tue,y=stars), alpha = 0.5)
ggplot(df.t) + geom_jitter(aes(x=Sat,y=stars), alpha = 0.5)

df.cui <- df.bus[,c("stars","categories")]
df.cui$categories <- gsub("[[:punct:]]+","",df.cui$categories)
df.cui <- df.cui %>% separate(categories, c(paste0('V',1:30)))
df.c <- df.cui %>% tidyr::gather(cases, word,2:31)
df.c <- df.c[which(complete.cases(df.c)),]
df.cf <- df.c %>% group_by(word) %>% summarise(n =n(), mean = mean(stars)) %>% as.data.frame()
df.cf$p <- df.cf$n / sum(df.cf$n)


library(tm)
library(wordcloud)
png("wordcloud_packages.png", width=12,height=8,res=300, units = 'in')
par(mar=rep(0,4))
wordcloud(df.cf$word, df.cf$n, random.order=F, min.freq=5, colors="#064293", scale=c(5,1), rot.per=0.15,vfont=c("sans serif","bold"))
dev.off()

head(df.cf[order(df.cf$n, decreasing = T),])
df.cf <- df.cf[-which(df.cf$word == "Restaurants" | df.cf$word == "Food"),]
png("wordcloud_packages1.png",width=12,height=8,res=300, units = 'in')
par(mar=rep(0,4))
wordcloud(df.cf$word, df.cf$n, random.order=F, min.freq=10, colors="#064293", scale=c(5,1), rot.per=0.15,vfont=c("sans serif","bold"))
dev.off()


category <- df.cf$word[df.cf$n>50]
df.cuisine <- df.c[df.c$word %in% category ,]
ggplot(df.cuisine) + geom_boxplot(aes(x=word, y = stars), fill="blue", alpha=0.5) + theme(axis.text.x = element_text(angle = 90, hjust = 1))

category <- df.cf$word[df.cf$n>300]
df.cuisine <- df.c[df.c$word %in% category ,]
ggplot(df.cuisine) + geom_boxplot(aes(x=word, y = stars), fill="blue", alpha=0.5)

#### Build Model ---------------------------------------------------------------------------------------------------------------
tomod <- df.bus[,c("name","business_id","RestaurantsGoodForGroups","RestaurantsTableService","RestaurantsReservations","review_count",
                   "WheelchairAccessible","HasTV","NoiseLevel","RestaurantsAttire","BusinessParking","hours.Saturday","categories","Caters","DriveThru","RestaurantsPriceRange2")]

muser <- df.rev[df.rev$user_id==muid,]
muser <- droplevels(muser)
buid <- muser$business_id
tomod <- tomod[tomod$business_id %in% buid,]
tomod <- droplevels(tomod)
table(complete.cases(tomod))


tomod[,category] <- 0
tomod$categories <- gsub("Brunch","Breakfast",tomod$categories)
tomod$categories <- gsub("Tea","Coffee",tomod$categories)
tomod$categories <- gsub("Sandwiches","Pizza",tomod$categories)

for (i in 1:17){
  tomod[which(grepl(category[i], tomod$categories)), category[i]] <- 1
}
tomod$categories <- NULL
tomod$Brunch <- NULL
tomod$Tea <- NULL
tomod$Sandwiches <- NULL
tomod$BusinessParking <- NULL
tomod <- tomod %>% separate(hours.Saturday, c("SatFrom","SatTo"), sep="-")

tomod$SatTo[tomod$SatTo==0.00] <- 23.99
tomod <- tomod[which(complete.cases(tomod)),]
tomod$SatFrom <- as.numeric(gsub(":","\\.",tomod$SatFrom))
tomod$SatTo <- as.numeric(gsub(":","\\.",tomod$SatTo))

tomod$SatTo[tomod$SatFrom > tomod$SatTo] <- tomod$SatTo[tomod$SatFrom > tomod$SatTo]+24
tomod$Sat <- tomod$SatTo - tomod$SatFrom
tomod$SatFrom <- NULL
tomod$SatTo <- NULL
muser <- muser[,c("business_id","stars")]

tomod <- merge(x=tomod, y=muser, by.x = "business_id", by.y = "business_id")

tomod1 <- tomod
tomod1$business_id <- NULL
tomod1$name <- NULL
tomod1$SatFrom <- NULL
tomod1$SatTo <- NULL

mod <- lm(stars~., data=tomod1)
summary(mod)
RSS <- c(crossprod(mod$residuals))
MSE <- RSS/length(mod$residuals)
RMSE <- sqrt(MSE)
plot(mod1)

tomodlog <- tomod1
tomodlog$review_count <- log(tomodlog$review_count)

mod1 <- lm(stars~., data=tomodlog)
summary(mod1)
RSS1 <- c(crossprod(mod1$residuals))
MSE1 <- RSS1/length(mod1$residuals)
RMSE1 <- sqrt(MSE1)
plot(mod1)



tomodlog2 <- tomodlog
tomodlog2$RestaurantsTableService <- NULL
tomodlog2$Fast <- NULL
tomodlog2$Chicken <- NULL
mod2 <- lm(stars~., data=tomodlog2)
summary(mod2)
RSS2 <- c(crossprod(mod2$residuals))
MSE2 <- RSS2/length(mod2$residuals)
RMSE2 <- sqrt(MSE2)
plot(mod2)


library(MASS)
k <- stepAIC(mod2, direction = "both")

mod3 <- lm(stars~RestaurantsReservations+NoiseLevel+RestaurantsAttire+American+Bars+Chinese+Mexican+Traditional+Nightlife, data=tomodlog)

mod2.res <- resid(mod2)
plot(tomodlog2$stars, mod2.res)
mod2.pred <- predict(mod2)

mod3.res <- resid(mod3)
plot(tomodlog$stars, mod3.res)









#### Users & Review Analysis ----------------------------------------------------------------------------------------------------------

df.us <- read.csv("nevada_user.csv")
df.rev <- read.csv("nevada_review.csv")

uid <- df.us$user_id[df.us$review_count>5]

df.us <- df.us[df.us$user_id %in% uid,]
df.rev <- df.rev[df.rev$user_id %in% uid,]
df.us$yelping_since <- as.Date(df.us$yelping_since, format = "%Y-%m-%d")

#df.us.k <- df.us[,-c("X","friends","elite","name","user_id","yelping_since")]
df.us.k <- df.us %>% select(-one_of(c("X","friends","elite","name","user_id","yelping_since")))

library(stats)
library(ggbiplot)

log.df.us.k <- df.us.k
log.df.us.k <- log(log.df.us.k +1)
log.df.us.k$review_count <- log(log.df.us.k$review_count)

us.pca <- prcomp(df.us.k, center=T, scale.=T)
print(us.pca)
summary(us.pca)

log.us.pca <- prcomp(log.df.us.k, center=T, scale.=T)
print(log.us.pca)
summary(log.us.pca)
g <- ggbiplot(us.pca, obs.scale = 1, var.scale = 1, groups = df.us.k$elite)
g <- g + scale_color_discrete(name = '')
g <- g + theme(legend.direction = 'horizontal', 
               legend.position = 'top')
print(g)

log.df.us.k <- log.df.us.k[,-2]
log.us.pca.2 <- prcomp(log.df.us.k, center=T, scale.=T)
summary(log.us.pca.2)
clust <- kmeans(log.df.us.k, 5, nstart = 20)





















