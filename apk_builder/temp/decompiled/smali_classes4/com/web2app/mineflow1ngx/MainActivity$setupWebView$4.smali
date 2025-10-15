.class public final Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;
.super Landroid/webkit/WebChromeClient;
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
        "\u0000O\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0002\u0008\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0008\n\u0000\n\u0002\u0010\u000b\n\u0002\u0008\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u0011\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000*\u0001\u0000\u0008\n\u0018\u00002\u00020\u0001J\u001c\u0010\u0002\u001a\u00020\u00032\u0008\u0010\u0004\u001a\u0004\u0018\u00010\u00052\u0008\u0010\u0006\u001a\u0004\u0018\u00010\u0007H\u0016J\u0012\u0010\u0008\u001a\u00020\u00032\u0008\u0010\t\u001a\u0004\u0018\u00010\nH\u0016J\u001a\u0010\u000b\u001a\u00020\u00032\u0008\u0010\u000c\u001a\u0004\u0018\u00010\r2\u0006\u0010\u000e\u001a\u00020\u000fH\u0016J2\u0010\u0010\u001a\u00020\u00112\u0008\u0010\u0012\u001a\u0004\u0018\u00010\r2\u0014\u0010\u0013\u001a\u0010\u0012\n\u0012\u0008\u0012\u0004\u0012\u00020\u00160\u0015\u0018\u00010\u00142\u0008\u0010\u0017\u001a\u0004\u0018\u00010\u0018H\u0016\u00a8\u0006\u0019"
    }
    d2 = {
        "com/web2app/mineflow1ngx/MainActivity$setupWebView$4",
        "Landroid/webkit/WebChromeClient;",
        "onGeolocationPermissionsShowPrompt",
        "",
        "origin",
        "",
        "callback",
        "Landroid/webkit/GeolocationPermissions$Callback;",
        "onPermissionRequest",
        "request",
        "Landroid/webkit/PermissionRequest;",
        "onProgressChanged",
        "view",
        "Landroid/webkit/WebView;",
        "newProgress",
        "",
        "onShowFileChooser",
        "",
        "webView",
        "filePathCallback",
        "Landroid/webkit/ValueCallback;",
        "",
        "Landroid/net/Uri;",
        "fileChooserParams",
        "Landroid/webkit/WebChromeClient$FileChooserParams;",
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

    iput-object p1, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    .line 110
    invoke-direct {p0}, Landroid/webkit/WebChromeClient;-><init>()V

    return-void
.end method


# virtual methods
.method public onGeolocationPermissionsShowPrompt(Ljava/lang/String;Landroid/webkit/GeolocationPermissions$Callback;)V
    .locals 3
    .param p1, "origin"    # Ljava/lang/String;
    .param p2, "callback"    # Landroid/webkit/GeolocationPermissions$Callback;

    .line 139
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0, p2}, Lcom/web2app/mineflow1ngx/MainActivity;->access$setGeolocationCallback$p(Lcom/web2app/mineflow1ngx/MainActivity;Landroid/webkit/GeolocationPermissions$Callback;)V

    .line 140
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0, p1}, Lcom/web2app/mineflow1ngx/MainActivity;->access$setGeolocationOrigin$p(Lcom/web2app/mineflow1ngx/MainActivity;Ljava/lang/String;)V

    .line 142
    nop

    .line 143
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    check-cast v0, Landroid/content/Context;

    .line 144
    nop

    .line 142
    const-string v1, "android.permission.ACCESS_FINE_LOCATION"

    invoke-static {v0, v1}, Landroidx/core/content/ContextCompat;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    move-result v0

    if-nez v0, :cond_0

    .line 147
    if-eqz p2, :cond_1

    const/4 v0, 0x1

    const/4 v1, 0x0

    invoke-interface {p2, p1, v0, v1}, Landroid/webkit/GeolocationPermissions$Callback;->invoke(Ljava/lang/String;ZZ)V

    goto :goto_0

    .line 149
    :cond_0
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getLocationPermissionLauncher$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroidx/activity/result/ActivityResultLauncher;

    move-result-object v0

    .line 151
    nop

    .line 152
    const-string v2, "android.permission.ACCESS_COARSE_LOCATION"

    filled-new-array {v1, v2}, [Ljava/lang/String;

    move-result-object v1

    .line 151
    nop

    .line 149
    invoke-virtual {v0, v1}, Landroidx/activity/result/ActivityResultLauncher;->launch(Ljava/lang/Object;)V

    .line 156
    :cond_1
    :goto_0
    return-void
.end method

.method public onPermissionRequest(Landroid/webkit/PermissionRequest;)V
    .locals 9
    .param p1, "request"    # Landroid/webkit/PermissionRequest;

    .line 159
    nop

    .line 160
    if-eqz p1, :cond_3

    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    move-object v1, p1

    .local v1, "permRequest":Landroid/webkit/PermissionRequest;
    const/4 v2, 0x0

    .line 161
    .local v2, "$i$a$-let-MainActivity$setupWebView$4$onPermissionRequest$1":I
    invoke-virtual {v1}, Landroid/webkit/PermissionRequest;->getResources()[Ljava/lang/String;

    move-result-object v3

    .line 162
    .local v3, "requestedResources":[Ljava/lang/String;
    invoke-static {v3}, Lkotlin/jvm/internal/Intrinsics;->checkNotNull(Ljava/lang/Object;)V

    array-length v4, v3

    const/4 v5, 0x0

    :goto_0
    if-ge v5, v4, :cond_2

    aget-object v6, v3, v5

    .line 163
    .local v6, "resource":Ljava/lang/String;
    nop

    .line 164
    const-string v7, "android.webkit.resource.VIDEO_CAPTURE"

    invoke-static {v6, v7}, Lkotlin/jvm/internal/Intrinsics;->areEqual(Ljava/lang/Object;Ljava/lang/Object;)Z

    move-result v7

    if-eqz v7, :cond_1

    .line 165
    nop

    .line 166
    move-object v7, v0

    check-cast v7, Landroid/content/Context;

    .line 167
    nop

    .line 165
    const-string v8, "android.permission.CAMERA"

    invoke-static {v7, v8}, Landroidx/core/content/ContextCompat;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    move-result v7

    if-nez v7, :cond_0

    .line 170
    invoke-static {v6}, Lkotlin/jvm/internal/Intrinsics;->checkNotNull(Ljava/lang/Object;)V

    filled-new-array {v6}, [Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v1, v7}, Landroid/webkit/PermissionRequest;->grant([Ljava/lang/String;)V

    goto :goto_1

    .line 172
    :cond_0
    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getCameraPermissionLauncher$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroidx/activity/result/ActivityResultLauncher;

    move-result-object v7

    invoke-virtual {v7, v8}, Landroidx/activity/result/ActivityResultLauncher;->launch(Ljava/lang/Object;)V

    .line 162
    .end local v6    # "resource":Ljava/lang/String;
    :cond_1
    :goto_1
    add-int/lit8 v5, v5, 0x1

    goto :goto_0

    .line 177
    :cond_2
    nop

    .line 160
    .end local v1    # "permRequest":Landroid/webkit/PermissionRequest;
    .end local v2    # "$i$a$-let-MainActivity$setupWebView$4$onPermissionRequest$1":I
    .end local v3    # "requestedResources":[Ljava/lang/String;
    nop

    .line 179
    :cond_3
    return-void
.end method

.method public onProgressChanged(Landroid/webkit/WebView;I)V
    .locals 3
    .param p1, "view"    # Landroid/webkit/WebView;
    .param p2, "newProgress"    # I

    .line 112
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getProgressBar$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroid/widget/ProgressBar;

    move-result-object v0

    const/4 v1, 0x0

    const-string v2, "progressBar"

    if-nez v0, :cond_0

    invoke-static {v2}, Lkotlin/jvm/internal/Intrinsics;->throwUninitializedPropertyAccessException(Ljava/lang/String;)V

    move-object v0, v1

    :cond_0
    invoke-virtual {v0, p2}, Landroid/widget/ProgressBar;->setProgress(I)V

    .line 113
    const/16 v0, 0x64

    if-ne p2, v0, :cond_2

    .line 114
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getProgressBar$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroid/widget/ProgressBar;

    move-result-object v0

    if-nez v0, :cond_1

    invoke-static {v2}, Lkotlin/jvm/internal/Intrinsics;->throwUninitializedPropertyAccessException(Ljava/lang/String;)V

    goto :goto_0

    :cond_1
    move-object v1, v0

    :goto_0
    const/16 v0, 0x8

    invoke-virtual {v1, v0}, Landroid/widget/ProgressBar;->setVisibility(I)V

    goto :goto_2

    .line 116
    :cond_2
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getProgressBar$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroid/widget/ProgressBar;

    move-result-object v0

    if-nez v0, :cond_3

    invoke-static {v2}, Lkotlin/jvm/internal/Intrinsics;->throwUninitializedPropertyAccessException(Ljava/lang/String;)V

    goto :goto_1

    :cond_3
    move-object v1, v0

    :goto_1
    const/4 v0, 0x0

    invoke-virtual {v1, v0}, Landroid/widget/ProgressBar;->setVisibility(I)V

    .line 118
    :goto_2
    return-void
.end method

.method public onShowFileChooser(Landroid/webkit/WebView;Landroid/webkit/ValueCallback;Landroid/webkit/WebChromeClient$FileChooserParams;)Z
    .locals 3
    .param p1, "webView"    # Landroid/webkit/WebView;
    .param p2, "filePathCallback"    # Landroid/webkit/ValueCallback;
    .param p3, "fileChooserParams"    # Landroid/webkit/WebChromeClient$FileChooserParams;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/webkit/WebView;",
            "Landroid/webkit/ValueCallback<",
            "[",
            "Landroid/net/Uri;",
            ">;",
            "Landroid/webkit/WebChromeClient$FileChooserParams;",
            ")Z"
        }
    .end annotation

    .line 125
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v0, p2}, Lcom/web2app/mineflow1ngx/MainActivity;->access$setFileUploadCallback$p(Lcom/web2app/mineflow1ngx/MainActivity;Landroid/webkit/ValueCallback;)V

    .line 127
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.GET_CONTENT"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 128
    .local v0, "intent":Landroid/content/Intent;
    const-string v1, "android.intent.category.OPENABLE"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    .line 129
    const-string v1, "*/*"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 131
    iget-object v1, p0, Lcom/web2app/mineflow1ngx/MainActivity$setupWebView$4;->this$0:Lcom/web2app/mineflow1ngx/MainActivity;

    invoke-static {v1}, Lcom/web2app/mineflow1ngx/MainActivity;->access$getFileChooserLauncher$p(Lcom/web2app/mineflow1ngx/MainActivity;)Landroidx/activity/result/ActivityResultLauncher;

    move-result-object v1

    const-string v2, "Choose File"

    check-cast v2, Ljava/lang/CharSequence;

    invoke-static {v0, v2}, Landroid/content/Intent;->createChooser(Landroid/content/Intent;Ljava/lang/CharSequence;)Landroid/content/Intent;

    move-result-object v2

    invoke-virtual {v1, v2}, Landroidx/activity/result/ActivityResultLauncher;->launch(Ljava/lang/Object;)V

    .line 132
    const/4 v1, 0x1

    return v1
.end method
