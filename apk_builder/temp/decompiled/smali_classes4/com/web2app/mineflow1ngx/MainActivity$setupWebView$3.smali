.class public final Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$3;
.super Landroid/webkit/WebViewClient;
.source "MainActivity.kt"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/web2app/mineflow1ngx/MainActivity;->setupWebView()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = null
.end annotation

.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000\u001d\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000*\u0001\u0000\u0008\n\u0018\u00002\u00020\u0001J\u001c\u0010\u0002\u001a\u00020\u00032\u0008\u0010\u0004\u001a\u0004\u0018\u00010\u00052\u0008\u0010\u0006\u001a\u0004\u0018\u00010\u0007H\u0016\u00a8\u0006\u0008"
    }
    d2 = {
        "com/web2app/mineflow1ngx/MainActivity$setupWebView$3",
        "Landroid/webkit/WebViewClient;",
        "onPageFinished",
        "",
        "view",
        "Landroid/webkit/WebView;",
        "url",
        "",
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


# instance fields
.field final synthetic this$0:Lcom/web2app/mineflow1ngx/MainActivity;


# direct methods
.method constructor <init>(Lcom/web2app/mineflow1ngx/MainActivity;)V
    .locals 0
    .param p1, "$receiver"    # Lcom/web2app/mineflow1ngx/MainActivity;

    iput-object p1, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$3;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    .line 102
    invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V

    return-void
.end method


# virtual methods
.method public onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V
    .locals 3
    .param p1, "view"    # Landroid/webkit/WebView;
    .param p2, "url"    # Ljava/lang/String;

    .line 104
    invoke-super {p0, p1, p2}, Landroid/webkit/WebViewClient;->onPageFinished(Landroid/webkit/WebView;Ljava/lang/String;)V

    .line 105
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$3;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getProgressBar$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroid/widget/ProgressBar;

    move-result-object v0

    const/4 v1, 0x0

    if-nez v0, :cond_0

    const-string v0, "progressBar"

    invoke-static {v0}, Lkotlin/jvm/internal/Intrinsics;->throwUninitializedPropertyAccessException(Ljava/lang/String;)V

    move-object v0, v1

    :cond_0
    const/16 v2, 0x8

    invoke-virtual {v0, v2}, Landroid/widget/ProgressBar;->setVisibility(I)V

    .line 106
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$3;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getSwipeRefresh$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;

    move-result-object v0

    if-nez v0, :cond_1

    const-string v0, "swipeRefresh"

    invoke-static {v0}, Lkotlin/jvm/internal/Intrinsics;->throwUninitializedPropertyAccessException(Ljava/lang/String;)V

    goto :goto_0

    :cond_1
    move-object v1, v0

    :goto_0
    const/4 v0, 0x0

    invoke-virtual {v1, v0}, Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;->setRefreshing(Z)V

    .line 107
    return-void
.end method
