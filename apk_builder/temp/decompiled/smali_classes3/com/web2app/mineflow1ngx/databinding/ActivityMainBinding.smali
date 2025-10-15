.class public final Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;
.super Ljava/lang/Object;
.source "ActivityMainBinding.java"

# interfaces
.implements Landroidx/viewbinding/ViewBinding;


# instance fields
.field public final progressBar:Landroid/widget/ProgressBar;

.field private final rootView:Landroidx/constraintlayout/widget/ConstraintLayout;

.field public final swipeRefresh:Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;

.field public final webView:Landroid/webkit/WebView;


# direct methods
.method private constructor <init>(Landroidx/constraintlayout/widget/ConstraintLayout;Landroid/widget/ProgressBar;Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;Landroid/webkit/WebView;)V
    .locals 0
    .param p1, "rootView"    # Landroidx/constraintlayout/widget/ConstraintLayout;
    .param p2, "progressBar"    # Landroid/widget/ProgressBar;
    .param p3, "swipeRefresh"    # Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;
    .param p4, "webView"    # Landroid/webkit/WebView;

    .line 34
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 35
    iput-object p1, p0, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->rootView:Landroidx/constraintlayout/widget/ConstraintLayout;

    .line 36
    iput-object p2, p0, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->progressBar:Landroid/widget/ProgressBar;

    .line 37
    iput-object p3, p0, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->swipeRefresh:Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;

    .line 38
    iput-object p4, p0, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->webView:Landroid/webkit/WebView;

    .line 39
    return-void
.end method

.method public static bind(Landroid/view/View;)Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;
    .locals 6
    .param p0, "rootView"    # Landroid/view/View;

    .line 68
    sget v0, Lcom/web2app/mineflow1ngx/R$id;->progressBar:I

    .line 69
    .local v0, "id":I
    invoke-static {p0, v0}, Landroidx/viewbinding/ViewBindings;->findChildViewById(Landroid/view/View;I)Landroid/view/View;

    move-result-object v1

    check-cast v1, Landroid/widget/ProgressBar;

    .line 70
    .local v1, "progressBar":Landroid/widget/ProgressBar;
    if-eqz v1, :cond_2

    .line 74
    sget v0, Lcom/web2app/mineflow1ngx/R$id;->swipeRefresh:I

    .line 75
    invoke-static {p0, v0}, Landroidx/viewbinding/ViewBindings;->findChildViewById(Landroid/view/View;I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;

    .line 76
    .local v2, "swipeRefresh":Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;
    if-eqz v2, :cond_1

    .line 80
    sget v0, Lcom/web2app/mineflow1ngx/R$id;->webView:I

    .line 81
    invoke-static {p0, v0}, Landroidx/viewbinding/ViewBindings;->findChildViewById(Landroid/view/View;I)Landroid/view/View;

    move-result-object v3

    check-cast v3, Landroid/webkit/WebView;

    .line 82
    .local v3, "webView":Landroid/webkit/WebView;
    if-eqz v3, :cond_0

    .line 86
    new-instance v4, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;

    move-object v5, p0

    check-cast v5, Landroidx/constraintlayout/widget/ConstraintLayout;

    invoke-direct {v4, v5, v1, v2, v3}, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;-><init>(Landroidx/constraintlayout/widget/ConstraintLayout;Landroid/widget/ProgressBar;Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;Landroid/webkit/WebView;)V

    return-object v4

    .line 83
    :cond_0
    goto :goto_0

    .line 77
    .end local v3    # "webView":Landroid/webkit/WebView;
    :cond_1
    goto :goto_0

    .line 71
    .end local v2    # "swipeRefresh":Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;
    :cond_2
    nop

    .line 89
    .end local v1    # "progressBar":Landroid/widget/ProgressBar;
    :goto_0
    invoke-virtual {p0}, Landroid/view/View;->getResources()Landroid/content/res/Resources;

    move-result-object v1

    invoke-virtual {v1, v0}, Landroid/content/res/Resources;->getResourceName(I)Ljava/lang/String;

    move-result-object v1

    .line 90
    .local v1, "missingId":Ljava/lang/String;
    new-instance v2, Ljava/lang/NullPointerException;

    const-string v3, "Missing required view with ID: "

    invoke-virtual {v3, v1}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v2
.end method

.method public static inflate(Landroid/view/LayoutInflater;)Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;
    .locals 2
    .param p0, "inflater"    # Landroid/view/LayoutInflater;

    .line 49
    const/4 v0, 0x0

    const/4 v1, 0x0

    invoke-static {p0, v0, v1}, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->inflate(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Z)Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;

    move-result-object v0

    return-object v0
.end method

.method public static inflate(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Z)Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;
    .locals 2
    .param p0, "inflater"    # Landroid/view/LayoutInflater;
    .param p1, "parent"    # Landroid/view/ViewGroup;
    .param p2, "attachToParent"    # Z

    .line 55
    sget v0, Lcom/web2app/mineflow1ngx/R$layout;->activity_main:I

    const/4 v1, 0x0

    invoke-virtual {p0, v0, p1, v1}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;Z)Landroid/view/View;

    move-result-object v0

    .line 56
    .local v0, "root":Landroid/view/View;
    if-eqz p2, :cond_0

    .line 57
    invoke-virtual {p1, v0}, Landroid/view/ViewGroup;->addView(Landroid/view/View;)V

    .line 59
    :cond_0
    invoke-static {v0}, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->bind(Landroid/view/View;)Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;

    move-result-object v1

    return-object v1
.end method


# virtual methods
.method public bridge synthetic getRoot()Landroid/view/View;
    .locals 1

    .line 20
    invoke-virtual {p0}, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->getRoot()Landroidx/constraintlayout/widget/ConstraintLayout;

    move-result-object v0

    return-object v0
.end method

.method public getRoot()Landroidx/constraintlayout/widget/ConstraintLayout;
    .locals 1

    .line 44
    iget-object v0, p0, Lcom/web2app/mineflow1ngx/databinding/ActivityMainBinding;->rootView:Landroidx/constraintlayout/widget/ConstraintLayout;

    return-object v0
.end method
