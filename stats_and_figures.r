#Required packages
library(ggplot2)
library(emmeans)
library(nlme)
library(tidyr)

#Load in dataframe
df <- read.csv("/athena/listonlab/scratch/dje4001/pseudorabies_dataset")

#Prepare dataframe
df$uid<-paste(df$cage,df$subjectid,df$treatment) #Create unique identifier for each subject
st.err<-function(x){sd(x,na.rm=TRUE)/(sqrt(length(x)))}
df$treatment<-as.factor(df$treatment) 
levels(df$treatment)<-c("Vehicle","ChronicCORT") #rename levels
df_total_cells<-aggregate(n~uid,data=df,FUN="sum") #Generate total number of cells per brain for normalization
colnames(df_total_cells)[2]<-"total_cells"
df_aggregated<-aggregate(n~uid+treatment+location,data=df,FUN="sum")
df_aggregated<-df_aggregated[!(df_aggregated$n<=1),]#Threshold regions with only 1 cell in them
df_aggregated<-merge(df_aggregated,df_total_cells,by="uid")
df_aggregated$uid<-as.factor(df_aggregated$uid)
df_aggregated$location<-as.factor(df_aggregated$location)
df_aggregated$normalized_cell_count<-df_aggregated$n/df_aggregated$total_cells #Normalize by the total number of cells

#Wide format of data
df_temp<-df_aggregated[,-4:-5]
dfwide_region<-spread(df_temp,location,normalized_cell_count)
dfwide_region[is.na(dfwide_region)]<-0
write.csv(dfwide_region,"/athena/listonlab/scratch/dje4001/dfwide_region.csv",row.names=FALSE)
df_av<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN="mean")
dfwide<-spread(df_av,treatment,normalized_cell_count)

#Average +/- SEM across subjects
df_av<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN="mean")
df_err<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN=st.err)
df_av$error<-df_err$normalized_cell_count

#Metrixs nessesary for linear model
#Distribution of cell counts per animal per region
p<-ggplot(data=df_av,aes(x=log10(normalized_cell_count),group=treatment,fill=treatment))+
  geom_density(alpha=0.5)+
  xlab("log10(Normalized cell count)")+
  ylab("Kernel Density")+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black"))
print(p)

#Main model
model1<-lme(log10(normalized_cell_count)~location,random=~1|uid,data=df_aggregated)

#Model measures of fit
r<-data.frame(residuals(model1))
r$r<-as.numeric(r$r)
p<-ggplot(data=r,aes(x=1,y=r,color=r,fill=r))+geom_jitter(size=3,alpha=0.4,width=0.01)+
  geom_hline(yintercept=0,linetype="dashed",size=1)+
  ylab("Linear Mixed Effects Model Residuals")+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black"),
        legend.position="none",axis.ticks.x=element_blank(),axis.text.x=element_blank(),axis.title.x=element_blank())
print(p)

#Plot a correlation of CORT and Vehicle
dfwide$significance<-ifelse((dfwide$Vehicle > 0.02) | (dfwide$ChronicCORT>0.02), "Largechange","NoChange")
p<-ggplot(data=dfwide,aes(x=Vehicle,y=ChronicCORT))+
  geom_point(aes(color=significance))+
  scale_color_manual(values=c("red","grey"))+
  theme(legend.position = "none")+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black"))+
  geom_text_repel(data=subset(dfwide,((Vehicle>0.02) | (ChronicCORT>0.2))),
                  aes(label=location),
                  size=5,
                  box.padding=unit(0.35,"lines"),
                  point.padding=unit(0.3,"lines"))
print(p)








#### OLDer

#Loop through plot over levels
p<-list()
for (i in colnames(df)){
  if (grepl("lv",i) || grepl("loc",i)){
    df_aggregated<-aggregate(n~uid+treatment+unlist(df[i]),data=df,FUN="sum") 
    df_aggregated_mean<-aggregate(n~treatment+unlist(df[i]),data=df,FUN="mean")
    df_aggregated_error<-aggregate(n~treatment+unlist(df[i]),data=df,FUN=st.err)
    df_aggregated_mean$error<-df_aggregated_error$n
    
    p[[i]]<-ggplot(data=df_aggregated_mean,aes(y=`unlist(df[i])`,x=n, 
                                     color=treatment,fill=treatment,group=treatment))+
      geom_point(stat="identity",position=position_dodge())+
      geom_errorbar(aes(xmin=n-error,xmax=n+error))+
      theme(panel.grid.major = element_blank(), #panel.grid.minor = element_blank(),
            panel.background = element_blank(), axis.line = element_line(colour = "black")) + 
      theme(legend.position = "none") 
    #print(p)
   
   #Generate correlation plot
   ce<-df_aggregated_mean[df_aggregated_mean$treatment=="CORTEXPERIMENTAL",]
   cc<-df_aggregated_mean[df_aggregated_mean$treatment=="CONTROL",]
   g<-ggplot(data=ce,aes(x=ce$n,y=cc$n))+
     geom_point()+
     scale_x_continuous(trans='log10')+
     scale_y_continuous(trans='log10')
   print(g)
  }}
do.call(grid.arrange,p)

df_total_cells<-aggregate(n~uid,data=df,FUN="sum")
colnames(df_total_cells)[2]="total_cells"
df2<-merge(df,df_total_cells,by="uid")
df2$normalized_cell_count<-df2$n/df2$total_cells
df<-df2
df$normalized_cell_count<-df$normalized_cell_count*10000

df_aggregated<-aggregate(normalized_cell_count~uid+treatment+location,data=df,FUN="sum") 

df_aggregated<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN="mean") 
p<-ggplot(data=df_aggregated,aes(x=n,y=location))+geom_bar(stat="identity")
print(p)

#distribution of the data
p<-ggplot(data=df_aggregated,aes(x=normalized_cell_count,group=uid,color=uid,fill=uid))+geom_density(alpha=0.5)
print(p)


df_aggregated<-aggregate(normalized_cell_count~uid+treatment+location,data=df,FUN="sum") 
df_aggregated_mean<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN="mean")
df_aggregated_error<-aggregate(normalized_cell_count~treatment+location,data=df_aggregated,FUN=st.err)
df_aggregated_mean$error<-df_aggregated_error$normalized_cell_count

p<-ggplot(data=df_aggregated_mean,aes(x=location,y=normalized_cell_count, 
                                           color=treatment,fill=treatment,group=treatment))+
  geom_point(size=5)+
  geom_point(size=4,fill="white")+
  geom_errorbar(aes(ymin=normalized_cell_count-error,ymax=normalized_cell_count+error))+
  theme(panel.grid.major = element_blank(), #panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black")) + 
  theme(legend.position = "none")+
  theme(axis.text.x=element_text(angle=90,vjust=0.5,hjust=1))
print(p)


#Mediodorsal nucleus of thalamus subset
md<-df[df$location=="Intermediodorsal nucleus of the thalamus" | df$location=="Mediodorsal nucleus of thalamus" |
         df$location=="Mediodorsal nucleus of the thalamus, central part" | df$location=="Mediodorsal nucleus of the thalamus, lateral part" |
         df$location=="Mediodorsal nucleus of the thalamus, medial part",]
md_sum<-aggregate(normalized_cell_count~uid+treatment,data=md,FUN="sum")
md_average<-aggregate(normalized_cell_count~treatment,data=md_sum,FUN="mean")
md_err<-aggregate(normalized_cell_count~treatment,data=md_sum,FUN=st.err)
md_average$error<-md_err$normalized_cell_count

p<-ggplot(data=md_average,aes(x=treatment,y=normalized_cell_count, color=treatment,fill=treatment,group=treatment))+
  geom_point(size=5)+
  geom_point(size=4,fill="white")+
  geom_errorbar(aes(ymin=normalized_cell_count-error,ymax=normalized_cell_count+error))+
  theme(panel.grid.major = element_blank(), #panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black")) + 
  theme(legend.position = "none")+
  theme(axis.text.x=element_text(angle=90,vjust=0.5,hjust=1))
print(p)


#Stats
df_aggregated<-aggregate(normalized_cell_count~uid+treatment+location,data=df,FUN="sum") 
fit<-glmer(normalized_cell_count~location+(1|uid),data=df_aggregated,family=Gamma(link="log"))

