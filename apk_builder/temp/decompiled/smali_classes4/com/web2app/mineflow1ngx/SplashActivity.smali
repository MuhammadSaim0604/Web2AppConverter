.class public final Lcom/web2app/mineflow1ngx/SplashActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "SplashActivity.kt"


# annotations
.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u0008\u0007\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0012\u0010\u0003\u001a\u00020\u00042\u0008\u0010\u0005\u001a\u0004\u0018\u00010\u0006H\u0014\u00a8\u0006\u0007"
    }
    d2 = {
        "Lcom/web2app/mineflow1ngx/SplashActivity;",
        "Landroidx/appcompat/app/AppCompatActivity;",
        "()V",
        "onCreate",
        "",
        "savedInstanceState",
        "Landroid/os/Bundle;",
        "app_debug"
    }
    k = 0x1
    mv = {
        0x1,
        0x9,
        0x0
    }
    xi = 0x30
.end annotation


# direct methods
.method public static synthetic $r8$lambda$O_043tQSeYaRVZT6cl1Fe5WRa5Q(Lcom/web2app/mineflow1ngx/SplashActivity;)V
    .locals 0

    invoke-static {p0}, Lcom/web2app/mineflow1ngx/SplashActivity;->onCreate$lambda$0(Lcom/web2app/mineflow1ngx/SplashActivity;)V

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 11
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    return-void
.end method

.method private static final onCreate$lambda$0(Lcom/web2app/mineflow1ngx/SplashActivity;)V
    .locals 3
    .param p0, "this$0"    # Lcom/web2app/mineflow1ngx/SplashActivity;

    const-string v0, "this$0"

    invoke-static {p0, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 18
    new-instance v0, Landroid/content/Intent;

    move-object v1, p0

    check-cast v1, Landroid/content/Context;

    const-class v2, Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    invoke-virtual {p0, v0}, Lcom/web2app/mineflow1ngx/SplashActivity;->startActivity(Landroid/content/Intent;)V

    .line 19
    invoke-virtual {p0}, Lcom/web2app/mineflow1ngx/SplashActivity;->finish()V

    .line 20
    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 14
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 15
    sget v0, Lcom/web2app/mineflow1ngx/R$layout;->activity_splash:I

    invoke-virtual {p0, v0}, Lcom/web2app/mineflow1ngx/SplashActivity;->setContentView(I)V

    .line 17
    new-instance v0, Landroid/os/Handler;

    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object v1

    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    new-instance v1, Lcom/web2app/mineflow1ngx/SplashActivity$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0}, Lcom/web2app/mineflow1ngx/SplashActivity$$ExternalSyntheticLambda0;-><init>(Lcom/web2app/mineflow1ngx/SplashActivity;)V

    .line 20
    nop

    .line 17
    const-wide/16 v2, 0x7d0

    invoke-virtual {v0, v1, v2, v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z

    .line 21
    return-void
.end method
