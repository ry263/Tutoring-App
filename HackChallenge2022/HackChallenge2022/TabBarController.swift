//
//  ViewController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/1/22.
//

import UIKit

class TabBar: UITabBarController {
    
    weak var user: User?
    var profileV : ProfileController!
    var searchV: CourseController!
    var notifV : NotificationController!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setUpTabBar()
    }
    
    
    func setUpTabBar() {
        
        if let user = self.user {
            profileV = ProfileController(ownAccount: true, user: self.user!)
            profileV.userViewing = self.user
            profileV.addTime = Availability(time: "+ Add a new time!", userID: user.id, ID: 1000000)
            
            searchV = CourseController(num: 0, user: self.user!)
            
            
            let searchController = createNavContoller(vc: searchV, selectedImage: UIImage(named: "shadowSearch.png")! , unselectedImage: UIImage(named: "search.png")!)
            
            let profileController = createNavContoller(vc: profileV, selectedImage: UIImage(named: "shadowProfile.png")! , unselectedImage: UIImage(named: "profile.png")!)
            
            viewControllers = [searchController, profileController]
            
            self.selectedIndex = 1
        }
        
        
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
