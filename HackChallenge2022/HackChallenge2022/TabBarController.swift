//
//  ViewController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/1/22.
//

import UIKit

class TabBar: UITabBarController {
    
    weak var user: User!
    var profileV : ProfileController!
    var searchV: CourseController!
    var notifV : NotificationController!
    
    convenience init(user: User) {
        self.init()
        
        self.user = user
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.selectedIndex = 2
        setUpTabBar()
    }
    
    
    func setUpTabBar() {
        
        profileV = ProfileController(ownAccount: true, user: self.user)
        profileV.userViewing = user
        profileV.addTime = Availability(time: "+ Add a new time!", userID: user.id, ID: 1000000)
        
        searchV = CourseController()
        notifV = NotificationController()
        notifV.user = self.user
        
        let notifController = createNavContoller(vc: notifV, selectedImage: UIImage(named: "shadowNotif.png")! , unselectedImage: UIImage(named: "notif.png")!)
        
        
        let searchController = createNavContoller(vc: searchV, selectedImage: UIImage(named: "shadowSearch.png")! , unselectedImage: UIImage(named: "search.png")!)
        
        let profileController = createNavContoller(vc: profileV, selectedImage: UIImage(named: "shadowProfile.png")! , unselectedImage: UIImage(named: "profile.png")!)
        
        viewControllers = [notifController, searchController, profileController]
        
    }
}

extension UITabBarController {
    func createNavContoller(vc : UIViewController, selectedImage: UIImage, unselectedImage: UIImage) -> UINavigationController {
        let viewController = vc
        let navController = UINavigationController(rootViewController: viewController)
        navController.tabBarItem.image = unselectedImage
        navController.tabBarItem.selectedImage = selectedImage
        return navController
    }
}
